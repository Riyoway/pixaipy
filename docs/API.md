# PixAI API — Unofficial Reference

**Version target:** PixAI web `app-1.0.2605` (analyzed 2026-10-26, 1,415 public
frontend chunks). Everything below was derived by read-only recon of
PixAI's own web application (`pixai.art` + `cdn.pixai.art`), cross-checked
against live API responses. Icons: ✅ verified against the live API ·
🔎 parsed from the official bundle (structure trusted) · ⚠️ inferred /
not implemented here.

> This is an undocumented, unofficial API. It can change at any time.
> The upstream web bundle currently registers **zero persisted-query
> hashes** — inline queries are the canonical send format today.

---

## 1. Transports

### 1.1 GraphQL ✅

```
POST https://api.pixai.art/graphql
Content-Type: application/json
```

Body envelope:

```json
{
  "operationName": "optionalButRecommended",
  "query": "mutation createGenerationTask($parameters: JSONObject!) { ... }",
  "variables": {},
  "extensions": { "clientLibrary": { "name": "@apollo/client", "version": "4.1.4" } }
}
```

- `extensions.clientLibrary` mirrors the official client (`4.1.3`/`4.1.4` both seen).
- Legacy `persistedQuery: {"version": 1, "sha256Hash": "<64 hex>"}` is accepted
  when you know a valid hash for the operation; on `PERSISTED_QUERY_NOT_FOUND`
  the request must be resent with the full inline `query`. Hashes used to be
  shipped inside the web bundle; the current bundle ships none, so inline is
  the default. One historically-verified hash survives and still works:
  `createGenerationTask` = `61b5dafa7ade64f847051cdca7024b359bae652421834b8f78423d7640f17d96`.

### 1.2 REST ✅

```
https://api.pixai.art/v1/...   (older, task-centric)
https://api.pixai.art/v2/...   (newer, platform paths)
Authorization: Bearer <token>
```

### 1.3 Authentication ✅

| How | Detail |
| --- | --- |
| Session token | Any GraphQL/REST call with `Authorization: Bearer <token>`. Your browser shows it as the **`Token` response header** (devtools → Network). |
| Token rotation 🔎 | The server may return a fresh `Token` response header on *any* call — clients should adopt it (the reference implementation does). |
| Access tokens 🔎 | Mutations `createAccessToken` / `revokeAccessToken` / `listMyAccessTokens` exist (the site's "API tokens" settings UI). Possibly a long-lived alternative to session tokens — **not yet verified here**. |
| Login mutation ✅ | Inline `mutation login($input: RegisterOrLoginInput!) { login(input: $input) { id email emailVerified } }`, `input: {email, password, recaptchaToken}`. **The token comes back as the `Token` response header**, not in the JSON. reCAPTCHA is required by design — supply a token your own browser session produced, or simply use token auth. |
| Session lifecycle 🔎 | `terminateSession`, `/v1/auth/logout`, `setupMFA`, `unlinkExternal`, `setPushToken` exist. |

### 1.4 Rate limiting & blocking ✅ (empirical)

- Sustained or bursty automation gets **blanket HTTP 500** answers (many
  requests in a row, regardless of token). Retrying aggressively deepens it.
  Gentle pacing (1–2 s between calls) plus short backoff is the working
  pattern; recovery appears to take tens of minutes to hours.
- Real errors otherwise arrive as GraphQL `errors[].extensions.code`.

---

## 2. GraphQL conventions

| Code | Meaning | Handling |
| --- | --- | --- |
| `UNAUTHENTICATED` (or HTTP 401/403) ✅ | dead/rotated token, or (as observed) the account is gone | refresh token or re-login; for a *deleted* account nothing restores it |
| `PERSISTED_QUERY_NOT_FOUND` 🔎 | hash drift | resend with inline `query` and no `persistedQuery` |
| blanket `HTTP 500` ✅ | rate-limit / shield | slow down, back off, wait |
| `HTTP 200 + data: null` ✅ | some mutations no-op silently when required variables are absent | always send variables explicitly |

Pagination 🔎: connection-style — `edges/node/pageInfo{hasNextPage…endCursor}` plus `before/after/first/last/orderBy` variables.

---

## 3. Verified recipes (send-as-is)

### 3.1 Account summary / credit balance ✅

```json
{ "query": "query getMyQuota { me { id quotaAmount } }", "variables": {} }
```
→ `data.me.quotaAmount` (int credits). An `email` field is also present on `me`
in most bundle queries (🔎) but the verified minimal shape is `id`+`quotaAmount`.

### 3.2 Submit a generation task ✅

```json
{
  "operationName": "createGenerationTask",
  "variables": {
    "parameters": {
      "prompts": "<prompt text>",
      "extra": { "naturalPrompts": "<prompt text>" },
      "priority": 1000,
      "width": 832, "height": 1216,
      "modelId": "<model id string>",
      "negativePrompts": "",
      "samplingSteps": 33,
      "samplingMethod": "Euler a",
      "cfgScale": 5,
      "seed": "",
      "clipSkip": 2,
      "batchSize": 4,
      "lora": {},
      "enableADetailer": true,
      "controlNets": [],
      "lightning": false,
      "promptHelper": { "withStage": false, "userWantToEnable": false, "enable": false }
    }
  },
  "query": "mutation createGenerationTask($parameters: JSONObject!) { createGenerationTask(parameters: $parameters) { ...TaskBase } } ..." 
}
```

Parameter notes (✅ verified against the live API):

| key | type | notes |
| --- | --- | --- |
| `modelId` | string | **required**, from your model list (also discoverable via `listGenerationModels` / `generationModel` REST presets) |
| `width`/`height` | int | match the model's supported resolutions (e.g. 832×1216, 1280×768) |
| `samplingMethod` | string | `"Euler a"` and friends — same strings the web UI sends |
| `seed` | int or empty string | empty = random |
| `batchSize` | int | images per task (costs ×batch) |
| `lora` | object | `{ "<loraModelId>": weight, ... }` or omitted |
| `priority` | int | official UI sends `1000` |

Response: the created task object (`.data.createGenerationTask` with `id`,
`status`, `parameters`, ...).

### 3.3 Task status via REST ✅

```
GET https://api.pixai.art/v1/task/<task_id>      # Bearer auth
```

- `status`: `"completed"`, `"failed"` observed at REST; in-progress values
  (`waiting`/`running`) appear while queued/running.
- On completion the images are in `outputs.mediaUrls[]` (plain URLs).
- `status == "failed"` carries a failure reason in the payload.

### 3.4 Media / files (img2img inputs etc.) 🔎 — flow not yet implemented

1. `mutation uploadFileMultiPart($step: UploadMultiPartStep!, $input: UploadMultiPartInput!)` → returns `uploadId` / `uploadUrl` / `exists` (two-step multipart handshake: `step` distinguishes the two calls)
2. PUT the bytes to the returned `uploadUrl`
3. `mutation uploadMedia($input: UploadMediaInput!)` → returns `mediaId` / `media{...}`
4. `query getFileUploadRecord($id)` / `listFiles` / `deleteFile` manage records

Passing the uploaded media into generation (image parameters) is done inside
`createGenerationTask.parameters` — exact key names not verified here yet.

---

## 4. GraphQL operation catalog

All operations below are **🔎 parsed from the official bundle ASTs**
(variable types included). ✅ marks the ones additionally verified executable.

### 4.1 Generation & tasks

| operation | type | variables | notes |
| --- | --- | --- | --- |
| `createGenerationTask` | mutation | `parameters: JSONObject!` | ✅ §3.2 |
| `cancelTask` | mutation | *(not in bundle AST)* | inline spelling observed working shape `{ cancelTask(taskId:) { id status } }`; ⚠️ best-effort |
| `getTaskById` | query | *(bundle AST)* | GraphQL twin of REST task status |
| `listMyTasks` / `listMyTasksTyped` | query | pageable | your task history ✅(shape) |
| `listTaskSummaries` | query | pageable | lighter summaries |
| `linkTaskToWorkspace` | mutation | `workspaceId: ID!, taskId: ID!` | |
| `archiveTrainingTask` | mutation | `id: ID!` | |
| `createTrainingTask` | mutation | `input: CreateTrainingTaskInput!` | LoRA training |
| `getTrainingTaskById` | query | | |

### 4.2 Account, auth & settings

| operation | type | variables | notes |
| --- | --- | --- | --- |
| `login` / `register` | mutation | `input: RegisterOrLoginInput!` | ✅ inline (needs `recaptchaToken`); not in bundle AST |
| `genCode` | mutation | `input: GenCodeInput!` | ✅ email-code sender (`intent: VerifyEmail`, `approach: Email`) |
| `verifyEmail` | mutation | `code: String` | ✅ |
| `getMyQuota`-style `me` queries | query | — | ✅ §3.1; see also `getMeWithQuotaForCurrency` |
| `updateMyInfo` | mutation | `input: UpdateUserInfoInput!` | |
| `setPreferences` / `setProfiles` | mutation | `value: JSONObject!` | |
| `upsertMySetting` / `getMySetting` / `listMySettings` / `deleteMySetting` | mutation/query | `type: UserSettingType!`, `data: JSONObject!` | persisted user settings blobs |
| `terminateSession` | mutation | `input: TerminateSessionInput!` | |
| `setupMFA` | mutation | `input: SetupMFAInput!` | |
| `checkUsername` / `getSuggestUsernames` | query | `username: String!` | onboarding helpers |
| `withdrawAccount` | mutation | `code: String, force: Boolean, cancel: Boolean` | ⚠️ **account deletion**. Bundle-shipped signature; variables must be non-empty or the mutation is a silent no-op (`data: null`). Not implemented by this library. |
| `createAccessToken` / `revokeAccessToken` | mutation | `input: CreateAccessTokenInput!` / `id: ID!` | API token management 🔎 |
| `listMyAccessTokens` / `listMySessions` / `listMyRoles` | query | pageable | |

### 4.3 Artworks & social

| operation | type | variables | notes |
| --- | --- | --- | --- |
| `getArtwork` / `getArtworkPreview` / `getArtworkWithTaskDetail` | query | `id: ID!, tackLanguage: String` | |
| `listArtworks` | query | pageable | global search/feed |
| `upsertArtwork` / `deleteArtwork` | mutation | `input: UpsertArtworkInput!, id, tackLanguage: String!` / `id: ID!` | publishing |
| `markArtwork` | mutation | `artworkId: ID!, type: MarkType!, target: Boolean!` | like etc. |
| `setFollowState` | mutation | `userId: ID!, target: Boolean!, private: Boolean` | |
| `setBlockState` | mutation | `userId: ID!, target: Boolean!` | |
| `getUserInfoById` / `getUserInfoByUsername` / `getUserProfileByUsername` | query | | |
| `getUserFollowCountsById` / `listUserFollowers` / `listUserFollowings` | query | pageable | |
| `getUserQuota` / `listUserQuotaLogs` | query | | others' / own credit logs |
| `listUserLikedArtworks` / `getUserArtworkLikedCount` | query | | |
| `getMedia` | query | | single media object |
| `listTacks` / `getTack` | query | | tag/curation system |
| `report` / `submitReview` | mutation | | content reporting/review |

### 4.4 Models & LoRAs

| operation | type | variables | notes |
| --- | --- | --- | --- |
| `listGenerationModels` | query | pageable | ✅ source of `model_id`s |
| `getGenerationModel` / `getGenerationModelPreview` | query | | |
| `listGenerationModelVersions` / `getGenerationModelByVersionId` / `getGenerationModelDetailByVersionId` | query | | versioned model data |
| `upsertGenerationModel` / `upsertGenerationModelVersion` / `deleteGenerationModel` | mutation | | model publishing |
| `markGenerationModel` | mutation | `modelId, type: GenerationModelMarkType!, target: Boolean!` | like etc. |
| `listLoraRecommendationsByModel` / `listSimilarLoras` | query | | LoRA recommendations |
| `listGenerationModelsWithTrainingTask` / `getPrivateGenerationModelTotalCount` | query | | your trained models |

### 4.5 Files & uploads

| operation | type | variables | notes |
| --- | --- | --- | --- |
| `uploadFileMultiPart` | mutation | `step: UploadMultiPartStep!, input: UploadMultiPartInput!` | 🔎 §3.4 |
| `uploadMedia` | mutation | `input: UploadMediaInput!` | 🔎 §3.4 |
| `getFile` / `getFileUploadRecord` / `listFiles` / `deleteFile` | query/mutation | `id: ID!` | record management |
| `getFileStatistics` | query | | |

### 4.6 Membership, payments, shop (informational)

`getMyMembership`, `getUserMembership`, `getAllPaymentItems`, `intentToPay` /
`intentToPayAntom`, `getOrderById`, `cancelOrder`, `purchaseDecoration`,
`listShopItems`, `listMyQuotaLogs`, `getMyShareCreditInfo`, `claimShareCredit`,
`createWebhook`/`listMyWebhooks` (outbound webhook URLs 🔎),
`getMyReferralCode`/`generateReferralCode`/`getReferralCodeInfo`/`getUserReferralLogs`,
`getUserYearWrappedStats`, collection-card sets — all 🔎 from the bundle.
Not covered by this library.

### 4.7 Moderation / admin (informational only)

`opBanUser`, `opShadowBanUser`, `opUnBanUser`, `opModerationNSFW`,
`opRefreshMediaSafetyScore`, `opRefreshTextSafetyScore`, `opResetUserAvatar/Cover`,
comment-turnstile toggles — staff-side operations 🔎; regular accounts cannot
use them.

### 4.8 Seasonal / chat / misc

`rollAprilFools2026Lottery`, `purchaseAprilFools2026Token`,
`listSpringPromotion2026LotteryRecords` (ephemeral event ops 🔎);
chat-workspace mutations/queries (chat editing scenes etc.);
`getWorkflowForMarketByWorkflowId`, `resetUserYearWrappedStats` …

*(The full, lossless machine-generated list — fields each operation selects —
lives in [`graphql-inventory.md`](graphql-inventory.md).)*

---

## 5. REST endpoint catalog

All 🔎 from the bundle, except ✅.

| endpoint | guess at purpose |
| --- | --- |
| `GET /v1/task/{id}` | ✅ task status (§3.3) |
| `POST /v1/auth/logout` | session teardown |
| `/v1/events/status` | event/campaign state |
| `/v1/kaisou/permission` | internal feature-flag/permission probe |
| `/v2/auth`, `/v2/oauth2` | auth/OAuth plumbing |
| `/v2/config` | runtime config |
| `GET /v2/generation-model/preset`, `/v2/generation-model/search` | model list/search (server-side presets) |
| `/v2/user/me/quota` | quota alternate (REST) — unverified |
| `/v2/user/me/tasks`, `/v2/user/me/task-stats` | task history/statistics |
| `/v2/user/me/notifications`, `…/unread-counts` | notifications |
| `/v2/artwork/feed/(following-news\|newest\|trending)` | artwork feeds |
| `/v2/artwork/recommend`, `/v2/artwork/recommend-visitor` | recommendations (signed-in / anonymous) |
| `/v2/order`, `/v2/payment`, `/v2/payment-account`, `/v2/purchase-recommendation` | payments (out of scope) |

---

## 6. Troubleshooting matrix

| Symptom | Cause | Fix |
| --- | --- | --- |
| `HTTP 401` / `UNAUTHENTICATED` 🚫 repeatedly | token rotated or expired | re-copy `Token` header from browser; the client auto-rotates on responses |
| `HTTP 500` on *everything* | rate-limit blanket (shield) | stop, wait 10–60+ min, resume slowly |
| `PERSISTED_QUERY_NOT_FOUND` | hash drift | resend inline (library does automatically) |
| `data: null` with no errors | mutation no-op (e.g. missing variables) | send variables explicitly |
| task stuck / never completes | — | poll `listMyTasks`/REST; use `cancelTask` best-effort |

---

## 7. Method & reproduction

- Source: public web bundles `https://cdn.pixai.art/artifacts/app-1.0.2605/assets/*.js`
  (1,415 chunks), read-only HTTP GETs mirroring what every browser does.
- Operation inventory was extracted from the minified Apollo document ASTs
  (operation name, variable definitions with types, selected fields).
- The reproduction method is intentionally simple — download the public
  chunks, locate the minified AST operation objects, and record names,
  types and selected fields of each operation.
- When PixAI ships a new bundle version, re-run the inventory and bump the
  header of this file.

---

*Licensing: this document describes facts observed in a public application.
Used at your own risk; respect PixAI's Terms of Service.*
