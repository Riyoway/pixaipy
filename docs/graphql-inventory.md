# GraphQL operation inventory — PixAI web bundle `app-1.0.2605`

Auto-generated on 2026-10-26 from a read-only parse of the public web
frontend bundles hosted on cdn.pixai.art.
`variables` are parsed from the operation ASTs; `fields` lists every
field the operation selects (deduplicated, first 10).

## REST endpoints found in the bundle

- `/v1/auth/logout`
- `/v1/events/status`
- `/v1/kaisou/permission`
- `/v2/artwork/feed/following-news`
- `/v2/artwork/feed/newest`
- `/v2/artwork/feed/trending`
- `/v2/artwork/recommend`
- `/v2/artwork/recommend-visitor`
- `/v2/auth`
- `/v2/config`
- `/v2/generation-model/preset`
- `/v2/generation-model/search`
- `/v2/oauth2`
- `/v2/order`
- `/v2/payment`
- `/v2/payment-account`
- `/v2/purchase-recommendation`
- `/v2/user/me/notifications`
- `/v2/user/me/notifications/unread-counts`
- `/v2/user/me/quota`
- `/v2/user/me/task-stats`
- `/v2/user/me/tasks`

## Operations

### mutation

| operation | variables | root field | fields… | chunk |
|---|---|---|---|---|
| `archiveTrainingTask` | `id: ID!` | `archiveTrainingTask` | `archiveTrainingTask` | `graphql-BRj5a0xt.js` |
| `cancelOrder` | `orderId: ID!` | `cancelOrder` | `cancelOrder` | `graphql-BRj5a0xt.js` |
| `claimShareCredit` | — | `getShareCredit` | `getShareCredit`, `amountEach`, `countRemains` | `graphql-BRj5a0xt.js` |
| `createAccessToken` | `input: CreateAccessTokenInput!` | `createAccessToken` | `createAccessToken`, `token`, `secret` | `graphql-BRj5a0xt.js` |
| `createChatEditingSceneTask` | `input: CreateChatEditingSceneTaskInput!` | `createChatEditingSceneTask` | `createChatEditingSceneTask`, `id` | `graphql-BRj5a0xt.js` |
| `createChatWorkspace` | `initialImage: String!`, `title: String` | `createChatWorkspace` | `createChatWorkspace`, `id`, `userId`, `title`, `initialImage`, `private` | `graphql-BRj5a0xt.js` |
| `createGenerationTask` | `parameters: JSONObject!` | `createGenerationTask` | `createGenerationTask` | `graphql-BRj5a0xt.js` |
| `createTrainingTask` | `input: CreateTrainingTaskInput!` | `createTrainingTask` | `createTrainingTask` | `graphql-BRj5a0xt.js` |
| `createWebhook` | `input: CreateWebhookInput!` | `createWebhook` | `createWebhook`, `webhookId`, `webhook` | `graphql-BRj5a0xt.js` |
| `deleteArtwork` | `id: ID!` | `deleteArtwork` | `deleteArtwork` | `graphql-BRj5a0xt.js` |
| `deleteChatWorkspace` | `workspaceId: ID!` | `deleteChatWorkspace` | `deleteChatWorkspace` | `graphql-BRj5a0xt.js` |
| `deleteFile` | `id: ID!` | `deleteFile` | `deleteFile` | `graphql-BRj5a0xt.js` |
| `deleteGenerationModel` | `id: ID!` | `deleteGenerationModel` | `deleteGenerationModel` | `graphql-BRj5a0xt.js` |
| `deleteMySetting` | `id: ID!` | `deleteSetting` | `deleteSetting` | `graphql-BRj5a0xt.js` |
| `deleteWebhook` | `id: ID!` | `deleteWebhook` | `deleteWebhook` | `graphql-BRj5a0xt.js` |
| `genCode` | `input: GenCodeInput!` | `genCode` | `genCode` | `graphql-BRj5a0xt.js` |
| `generateReferralCode` | — | `generateReferralCode` | `generateReferralCode`, `id`, `code`, `type` | `graphql-BRj5a0xt.js` |
| `intentToPay` | `itemId: String!`, `interval: Interval`, `opt: PaymentOpt` | `intentToPay` | `intentToPay` | `graphql-BRj5a0xt.js` |
| `intentToPayAntom` | `itemId: String!`, `interval: Interval`, `opt: PaymentOpt` | `intentToPay` | `intentToPay` | `graphql-BRj5a0xt.js` |
| `linkTaskToWorkspace` | `workspaceId: ID!`, `taskId: ID!` | `linkTaskToWorkspace` | `linkTaskToWorkspace` | `graphql-BRj5a0xt.js` |
| `markArtwork` | `artworkId: ID!`, `type: MarkType!`, `target: Boolean!` | `markArtwork` | `markArtwork` | `graphql-BRj5a0xt.js` |
| `markGenerationModel` | `modelId: ID!`, `type: GenerationModelMarkType!`, `target: Boolean!` | `markGenerationModel` | `markGenerationModel` | `graphql-BRj5a0xt.js` |
| `opBanUser` | `id: ID!` | `opBanUser` | `opBanUser` | `graphql-BRj5a0xt.js` |
| `opModerationNSFW` | `input: ModerationNSFWInput!` | `opModerationNSFW` | `opModerationNSFW` | `graphql-BRj5a0xt.js` |
| `opRefreshMediaSafetyScore` | `input: RefreshMediaSafetyScoreInput!` | `opRefreshMediaSafetyScore` | `opRefreshMediaSafetyScore`, `artworkId`, `mediaSafetyScore` | `graphql-BRj5a0xt.js` |
| `opRefreshTextSafetyScore` | `input: RefreshTextSafetyScoreInput!` | `opRefreshTextSafetyScore` | `opRefreshTextSafetyScore`, `artworkId`, `modelId`, `textSafetyScore` | `graphql-BRj5a0xt.js` |
| `opRemoveCommentTurnstile` | `id: ID!` | `opRemoveCommentTurnstile` | `opRemoveCommentTurnstile` | `graphql-BRj5a0xt.js` |
| `opRequireCommentTurnstile` | `id: ID!` | `opRequireCommentTurnstile` | `opRequireCommentTurnstile` | `graphql-BRj5a0xt.js` |
| `opResetUserAvatar` | `userId: ID!` | `opResetUserAvatar` | `opResetUserAvatar` | `graphql-BRj5a0xt.js` |
| `opResetUserCover` | `userId: ID!` | `opResetUserCover` | `opResetUserCover` | `graphql-BRj5a0xt.js` |
| `opShadowBanUser` | `id: ID!` | `opShadowBanUser` | `opShadowBanUser` | `graphql-BRj5a0xt.js` |
| `opUnBanUser` | `id: ID!` | `opUnBanUser` | `opUnBanUser` | `graphql-BRj5a0xt.js` |
| `purchaseAprilFools2026Token` | `quantity: Int` | `purchaseLotteryToken` | `purchaseLotteryToken` | `graphql-BRj5a0xt.js` |
| `purchaseDecoration` | `skuId: ID!` | `purchaseDecorationSku` | `purchaseDecorationSku`, `id`, `userId`, `skuId`, `decorationId`, `finalCredits`, `userMembershipTier`, `status`, `createdAt`, `updatedAt` | `graphql-BRj5a0xt.js` |
| `report` | `refId: ID!`, `refType: RefType!`, `reason: ReportReason!`, `extra: JSONObject` | `report` | `report` | `graphql-BRj5a0xt.js` |
| `resetUserYearWrappedStats` | `userId: ID!`, `year: Int!` | `recalculateUserYearWrappedStats` | `recalculateUserYearWrappedStats` | `graphql-BRj5a0xt.js` |
| `reviewMemberOnlyModelEarlyAccess` | `input: ReviewCommentInput!` | `reviewMemberOnlyModelEarlyAccess` | `reviewMemberOnlyModelEarlyAccess` | `graphql-BRj5a0xt.js` |
| `revokeAccessToken` | `id: ID!` | `revokeAccessToken` | `revokeAccessToken` | `graphql-BRj5a0xt.js` |
| `rollAprilFools2026Lottery` | — | `rollLottery` | `rollLottery`, `aprilFoolsEvent2026Reward`, `sign`, `creditReward`, `extraPackageBoostCode`, `extraPackageBoostPercentage`, `availableSince`, `availableUntil` | `graphql-BRj5a0xt.js` |
| `setBlockState` | `userId: ID!`, `target: Boolean!` | `setBlockState` | `setBlockState` | `graphql-BRj5a0xt.js` |
| `setFollowState` | `userId: ID!`, `target: Boolean!`, `private: Boolean` | `setFollowState` | `setFollowState` | `graphql-BRj5a0xt.js` |
| `setPreferences` | `value: JSONObject!` | `setPreferences` | `setPreferences` | `graphql-BRj5a0xt.js` |
| `setProfiles` | `value: JSONObject!` | `setProfiles` | `setProfiles` | `graphql-BRj5a0xt.js` |
| `setPushToken` | `token: String!`, `withdraw: Boolean` | `setPushToken` | `setPushToken`, `acknowledged` | `graphql-BRj5a0xt.js` |
| `setReferrer` | `code: String!` | `setReferrer` | `setReferrer` | `graphql-BRj5a0xt.js` |
| `setupMFA` | `input: SetupMFAInput!` | `setupMFA` | `setupMFA`, `url`, `recoveryCode` | `graphql-BRj5a0xt.js` |
| `submitReview` | `input: ReviewInput!` | `review` | `review` | `graphql-BRj5a0xt.js` |
| `terminateSession` | `input: TerminateSessionInput!` | `terminateSession` | `terminateSession` | `graphql-BRj5a0xt.js` |
| `toggleDecoration` | `decorationId: ID!`, `enabled: Boolean!` | `toggleDecorationV2` | `toggleDecorationV2`, `id`, `isEnabled` | `graphql-BRj5a0xt.js` |
| `unlinkExternal` | `type: String!` | `unlinkExternal` | `unlinkExternal` | `graphql-BRj5a0xt.js` |
| `updateChatTaskReaction` | `workspaceId: ID!`, `taskId: ID!`, `mediaId: String!`, `likeOrDislike: Boolean` | `updateChatTaskReaction` | `updateChatTaskReaction`, `taskId`, `mediaId`, `likeOrDislike` | `graphql-BRj5a0xt.js` |
| `updateChatWorkspace` | `workspaceId: ID!`, `title: String!` | `updateChatWorkspace` | `updateChatWorkspace`, `createdAt`, `id`, `initialImage`, `private`, `title`, `updatedAt`, `userId` | `graphql-BRj5a0xt.js` |
| `updateMyInfo` | `input: UpdateUserInfoInput!` | `updateUserInfo` | `updateUserInfo` | `graphql-BRj5a0xt.js` |
| `updateUserSensitiveInfos` | `input: UpdateUserSensitiveInfosInput!` | `updateUserSensitiveInfos` | `updateUserSensitiveInfos` | `graphql-BRj5a0xt.js` |
| `uploadFileMultiPart` | `step: UploadMultiPartStep!`, `input: UploadMultiPartInput!` | `uploadFileMultiPart` | `uploadFileMultiPart`, `uploadId`, `uploadUrl`, `exists` | `graphql-BRj5a0xt.js` |
| `uploadMedia` | `input: UploadMediaInput!` | `uploadMedia` | `uploadMedia`, `uploadUrl`, `externalId`, `mediaId`, `media` | `graphql-BRj5a0xt.js` |
| `upsertArtwork` | `input: UpsertArtworkInput!`, `id: ID`, `tackLanguage: String!` | `upsertArtwork` | `upsertArtwork`, `tacks`, `nominatedTacks`, `tackId`, `inputName`, `status` | `graphql-BRj5a0xt.js` |
| `upsertGenerationModel` | `id: ID`, `input: UpsertGenerationModelInput!` | `upsertGenerationModel` | `upsertGenerationModel` | `graphql-BRj5a0xt.js` |
| `upsertGenerationModelVersion` | `id: ID`, `input: UpsertGenerationModelVersionInput!` | `upsertGenerationModelVersion` | `upsertGenerationModelVersion`, `model` | `graphql-BRj5a0xt.js` |
| `upsertMySetting` | `id: ID`, `type: UserSettingType!`, `data: JSONObject!` | `upsertSetting` | `upsertSetting`, `id`, `type`, `data` | `graphql-BRj5a0xt.js` |
| `verifyEmail` | `code: String` | `verifyEmail` | `verifyEmail` | `graphql-BRj5a0xt.js` |
| `withdrawAccount` | `code: String`, `force: Boolean`, `cancel: Boolean` | `withdrawAccount` | `withdrawAccount` | `graphql-BRj5a0xt.js` |
### query

| operation | variables | root field | fields… | chunk |
|---|---|---|---|---|
| `checkUsername` | `username: String!` | `checkUsername` | `checkUsername`, `valid`, `reason` | `graphql-BRj5a0xt.js` |
| `getAllPaymentItems` | `type: PaymentItemType`, `promotionOption: PromotionOption` | `paymentItems` | `paymentItems`, `id`, `planId`, `tier`, `type`, `prices`, `interval`, `promotionalCode`, `currencies`, `amount` | `graphql-BRj5a0xt.js` |
| `getAprilFools2026LotteryRewards` | `before: String`, `after: String`, `first: Int`, `last: Int`, `userId: ID` | `lotteries` | `lotteries`, `edges`, `node`, `cursor`, `pageInfo` | `graphql-BRj5a0xt.js` |
| `getArtwork` | `id: ID!`, `tackLanguage: String` | `artwork` | `artwork` | `graphql-BRj5a0xt.js` |
| `getArtworkPreview` | `id: ID!`, `tackLanguage: String` | `artwork` | `artwork` | `graphql-BRj5a0xt.js` |
| `getArtworkWithTaskDetail` | `id: ID!`, `tackLanguage: String` | `artwork` | `artwork` | `graphql-BRj5a0xt.js` |
| `getChatEditingModels` | — | `chatEditingModels` | `chatEditingModels`, `modelId`, `name`, `available` | `graphql-BRj5a0xt.js` |
| `getChatEditingScene` | `sceneId: String!` | `chatEditingScene` | `chatEditingScene` | `graphql-BRj5a0xt.js` |
| `getChatTaskReactionByWorkspace` | `workspaceId: ID!` | `chatTaskReactionByWorkspace` | `chatTaskReactionByWorkspace` | `graphql-BRj5a0xt.js` |
| `getChatWorkspace` | `id: ID!` | `chatWorkspace` | `chatWorkspace` | `graphql-BRj5a0xt.js` |
| `getChatWorkspaceTasks` | `workspaceId: ID!`, `before: String`, `after: String`, `first: Int`, `last: Int`, `orderBy: String` | `chatWorkspaceTasks` | `chatWorkspaceTasks`, `totalCount`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `edges`, `node` | `graphql-BRj5a0xt.js` |
| `getDecoration` | `id: ID`, `code: String` | `decoration` | `decoration` | `graphql-BRj5a0xt.js` |
| `getFile` | `id: ID!` | `fileUploadRecord` | `fileUploadRecord` | `graphql-BRj5a0xt.js` |
| `getFileStatistics` | `userId: ID!`, `scope: String`, `q: String` | `fileStatistics` | `fileStatistics` | `graphql-BRj5a0xt.js` |
| `getFileUploadRecord` | `id: ID!` | `fileUploadRecord` | `fileUploadRecord` | `graphql-BRj5a0xt.js` |
| `getGenerationModel` | `id: ID!` | `generationModel` | `generationModel` | `graphql-BRj5a0xt.js` |
| `getGenerationModelByVersionId` | `id: ID!` | `generationModelVersion` | `generationModelVersion`, `model`, `refCount`, `curations` | `graphql-BRj5a0xt.js` |
| `getGenerationModelDetailByVersionId` | `id: ID!` | `generationModelVersion` | `generationModelVersion`, `model` | `graphql-BRj5a0xt.js` |
| `getGenerationModelPreview` | `id: ID!` | `generationModel` | `generationModel` | `graphql-BRj5a0xt.js` |
| `getMedia` | `id: String!` | `media` | `media` | `graphql-BRj5a0xt.js` |
| `getMeWithQuotaForCurrency` | `currency: String!` | `me` | `me`, `quotaAmount` | `graphql-BRj5a0xt.js` |
| `getMyExternalProfiles` | — | `me` | `me`, `id`, `externalProfiles` | `graphql-BRj5a0xt.js` |
| `getMyMembership` | — | `me` | `me`, `id`, `membership`, `subscription` | `graphql-BRj5a0xt.js` |
| `getMyPreferences` | — | `me` | `me`, `id`, `preferences` | `graphql-BRj5a0xt.js` |
| `getMyReferralCode` | — | `me` | `me`, `id`, `referralCode`, `code`, `type` | `graphql-BRj5a0xt.js` |
| `getMyReferrerId` | — | `me` | `me`, `id`, `referrerId` | `graphql-BRj5a0xt.js` |
| `getMyRoles` | `before: String`, `after: String`, `first: Int`, `last: Int`, `names: [String!]` | `me` | `me`, `id`, `roles`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor` | `graphql-BRj5a0xt.js` |
| `getMySetting` | `id: ID!` | `setting` | `setting`, `id`, `type`, `data` | `graphql-BRj5a0xt.js` |
| `getMySettingLimit` | `type: UserSettingType!` | `me` | `me`, `id`, `settingLimit` | `graphql-BRj5a0xt.js` |
| `getMyShareCreditInfo` | — | `me` | `me`, `id`, `shareCreditInfo`, `amountEach`, `countRemains` | `graphql-BRj5a0xt.js` |
| `getNeedCommentTurnstile` | — | `needCommentTurnstile` | `needCommentTurnstile` | `graphql-BRj5a0xt.js` |
| `getOrderById` | `orderId: ID!` | `order` | `order`, `id`, `userId`, `itemId`, `provider`, `externalId`, `status`, `amount`, `currency`, `extra` | `graphql-BRj5a0xt.js` |
| `getPrivateGenerationModelTotalCount` | `authorId: ID`, `type: GenerationModelType`, `isPrivate: Boolean` | `generationModels` | `generationModels`, `totalCount` | `graphql-BRj5a0xt.js` |
| `getReferralCodeInfo` | `referCode: String!` | `referralCode` | `referralCode`, `userId`, `firstPurchaseRewardCredits` | `graphql-BRj5a0xt.js` |
| `getShopItem` | `id: ID!` | `decorationSku` | `decorationSku` | `graphql-BRj5a0xt.js` |
| `getSuggestUsernames` | — | `suggestUsernames` | `suggestUsernames` | `graphql-BRj5a0xt.js` |
| `getTack` | `id: ID`, `defaultName: String`, `codeName: String` | `tack` | `tack` | `graphql-BRj5a0xt.js` |
| `getTaskById` | `id: ID!` | `task` | `task` | `graphql-BRj5a0xt.js` |
| `getTrainingTaskById` | `id: ID!` | `trainingTask` | `trainingTask` | `graphql-BRj5a0xt.js` |
| `getUserArtworkLikedCount` | `userId: ID!` | `user` | `user`, `id`, `artworkLikedCount` | `graphql-BRj5a0xt.js` |
| `getUserBlockList` | `before: String`, `after: String`, `first: Int`, `last: Int` | `me` | `me`, `blockList`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor` | `graphql-BRj5a0xt.js` |
| `getUserCardSetProgress` | `userId: ID!`, `collectionCardSetId: ID`, `collectionCardSetCode: String` | `user` | `user`, `id`, `collectionCardSetProgress`, `collectionCardSet`, `totalCollectionCards`, `ownedCollectionCards` | `graphql-BRj5a0xt.js` |
| `getUserFollowCountsById` | `userId: ID!` | `user` | `user`, `id`, `followerCount`, `followingCount` | `graphql-BRj5a0xt.js` |
| `getUserInfoById` | `userId: ID!` | `user` | `user` | `graphql-BRj5a0xt.js` |
| `getUserInfoByUsername` | `username: String!` | `user` | `user`, `artworkLikedCount` | `graphql-BRj5a0xt.js` |
| `getUserMembership` | `userId: ID!` | `user` | `user`, `id`, `membership`, `subscription` | `graphql-BRj5a0xt.js` |
| `getUserProfileByUsername` | `username: String!` | `user` | `user`, `id`, `profiles` | `graphql-BRj5a0xt.js` |
| `getUserProfiles` | `userId: ID!` | `user` | `user`, `id`, `profiles` | `graphql-BRj5a0xt.js` |
| `getUserQuota` | `userId: ID!` | `user` | `user`, `id` | `graphql-BRj5a0xt.js` |
| `getUserReferralLogs` | `before: String`, `after: String`, `first: Int`, `last: Int`, `orderBy: String`, `referrerId: ID` | `referralLogs` | `referralLogs`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `edges`, `cursor`, `node`, `id` | `graphql-BRj5a0xt.js` |
| `getUserRoles` | `userId: ID!`, `names: [String!]`, `before: String`, `after: String`, `first: Int`, `last: Int` | `user` | `user`, `id`, `roles`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor` | `graphql-BRj5a0xt.js` |
| `getUserYearWrappedStats` | `userId: ID!`, `year: Int!` | `user` | `user`, `yearWrappedStats`, `status`, `generatedImageCount`, `publishedArtworkCount`, `receivedLikeCount`, `receivedCommentCount`, `membershipDays`, `membershipTimeSavedInSeconds`, `membershipCreditsSaved` | `graphql-BRj5a0xt.js` |
| `getWorkflowForMarketByWorkflowId` | `workflowId: ID!`, `tackLanguage: String` | `workflow` | `workflow`, `artwork` | `graphql-BRj5a0xt.js` |
| `listActiveCollectionCardSets` | `type: CollectionCardSetType`, `before: String`, `after: String`, `first: Int`, `last: Int` | `activeCollectionCardSets` | `activeCollectionCardSets`, `edges`, `node`, `id`, `code`, `name`, `type`, `status`, `description`, `collectionCards` | `graphql-BRj5a0xt.js` |
| `listArtworks` | `before: String`, `after: String`, `first: Int`, `last: Int`, `orderBy: String`, `tag: String`, `tackId: String`, `q: String`, `relevantArtworkId: ID`, `keyword: String`, `text: String`, `hidePrompts: Boolean`, `isSafeSearch: Boolean`, `feed: String`, `authorId: ID`, `challenge: Int`, `archived: Boolean`, `visibilityType: ArtworkVisibilityType`, `i2vPro: Boolean`, `animatedBaseArtworkId: ID`, `modelId: ID`, `modelVersionId: ID`, `loraId: ID`, `loraVersionId: ID`, `workflowId: ID`, `workflowVersionId: ID`, `time: DateRange`, `type: ArtworkType`, `types: [ArtworkType]`, `rankMediaType: RankMediaType`, `tackLanguage: String` | `artworks` | `artworks`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `totalCount` | `graphql-BRj5a0xt.js` |
| `listCards` | `cardCodes: [String!]` | `collectionCardsByCodes` | `collectionCardsByCodes` | `graphql-BRj5a0xt.js` |
| `listChatEditingScenes` | — | `chatEditingScenes` | `chatEditingScenes` | `graphql-BRj5a0xt.js` |
| `listChatWorkspaces` | `before: String`, `after: String`, `first: Int`, `last: Int`, `orderBy: String`, `userId: ID` | `chatWorkspaces` | `chatWorkspaces`, `edges`, `node`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `totalCount` | `graphql-BRj5a0xt.js` |
| `listFiles` | `userId: ID!`, `scope: String`, `q: String`, `after: String`, `first: Int`, `before: String`, `last: Int`, `orderBy: String` | `files` | `files`, `edges`, `cursor`, `node`, `pageInfo` | `graphql-BRj5a0xt.js` |
| `listFourthAnniversary2026LotteryRecords` | `before: String`, `after: String`, `first: Int`, `last: Int` | `lotteries` | `lotteries`, `edges`, `node`, `id`, `extra`, `createdAt`, `pageInfo` | `graphql-BRj5a0xt.js` |
| `listGenerationModels` | `before: String`, `after: String`, `first: Int`, `last: Int`, `orderBy: String`, `tag: String`, `tackId: String`, `type: GenerationModelType`, `types: [GenerationModelType]`, `timeRange: DateRange`, `keyword: String`, `feed: String`, `authorId: ID`, `category: String`, `loraBaseModelTypes: [GenerationModelType!]`, `loraBaseModelIds: [ID!]`, `permittedUse: PermittedUse` | `generationModels` | `generationModels`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `totalCount` | `graphql-BRj5a0xt.js` |
| `listGenerationModelsWithTrainingTask` | `before: String`, `after: String`, `first: Int`, `last: Int`, `orderBy: String`, `type: GenerationModelType`, `types: [GenerationModelType]`, `timeRange: DateRange`, `feed: String`, `authorId: ID` | `generationModels` | `generationModels`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `totalCount` | `graphql-BRj5a0xt.js` |
| `listGenerationModelVersions` | `modelId: ID!`, `before: String`, `after: String`, `first: Int`, `last: Int`, `baseModelType: GenerationModelType`, `status: String` | `generationModelVersions` | `generationModelVersions`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `totalCount` | `graphql-BRj5a0xt.js` |
| `listLoraRecommendationsByModel` | `modelId: ID!`, `modelVersionId: ID`, `first: Int`, `retriever: LoraRetriever` | `recommendLorasByModel` | `recommendLorasByModel` | `graphql-BRj5a0xt.js` |
| `listMyAccessTokens` | `before: String`, `after: String`, `first: Int`, `last: Int` | `me` | `me`, `id`, `accessTokens`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor` | `graphql-BRj5a0xt.js` |
| `listMyActiveDecorations` | `id: ID`, `type: DecorationType` | `user` | `user`, `id`, `activeDecorations` | `graphql-BRj5a0xt.js` |
| `listMyBookmarkItems` | `before: String`, `after: String`, `first: Int`, `last: Int`, `orderBy: String`, `types: [RefType]` | `me` | `me`, `id`, `defaultBookmark`, `items`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage` | `graphql-BRj5a0xt.js` |
| `listMyDecorations` | `before: String`, `after: String`, `first: Int`, `last: Int`, `type: DecorationType`, `codes: [String!]` | `me` | `me`, `decorations`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor` | `graphql-BRj5a0xt.js` |
| `listMyQuotaLogs` | `currency: String`, `before: String`, `after: String`, `first: Int`, `last: Int` | `me` | `me`, `id`, `quotaLogs`, `totalCount`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `edges` | `graphql-BRj5a0xt.js` |
| `listMySessions` | `before: String`, `after: String`, `first: Int`, `last: Int`, `orderBy: String`, `isValid: Boolean` | `me` | `me`, `id`, `sessions`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor` | `graphql-BRj5a0xt.js` |
| `listMySettings` | `type: UserSettingType!`, `before: String`, `after: String`, `first: Int`, `last: Int` | `me` | `me`, `id`, `settings`, `edges`, `node`, `type`, `data`, `cursor`, `pageInfo`, `hasNextPage` | `graphql-BRj5a0xt.js` |
| `listMyTasks` | `status: String`, `before: String`, `after: String`, `first: Int`, `last: Int`, `parameterFields: [String!]` | `me` | `me`, `id`, `tasks`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `edges`, `node` | `graphql-BRj5a0xt.js` |
| `listMyTasksTyped` | `status: String`, `before: String`, `after: String`, `first: Int`, `last: Int` | `me` | `me`, `id`, `tasks`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `edges`, `node` | `graphql-BRj5a0xt.js` |
| `listMyWebhooks` | `before: String`, `after: String`, `first: Int`, `last: Int` | `me` | `me`, `id`, `webhooks`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor` | `graphql-BRj5a0xt.js` |
| `listShopItems` | `before: String`, `after: String`, `first: Int`, `last: Int`, `orderBy: String` | `activeDecorationSkus` | `activeDecorationSkus`, `pageInfo`, `edges`, `node` | `graphql-BRj5a0xt.js` |
| `listSimilarLoras` | `loraId: ID!`, `loraVersionId: ID`, `first: Int`, `retriever: LoraRetriever` | `recommendSimilarLoras` | `recommendSimilarLoras` | `graphql-BRj5a0xt.js` |
| `listSpringPromotion2026LotteryRecords` | `before: String`, `after: String`, `first: Int`, `last: Int` | `lotteries` | `lotteries`, `edges`, `node`, `id`, `extra`, `createdAt`, `updatedAt`, `pageInfo` | `graphql-BRj5a0xt.js` |
| `listTacks` | `before: String`, `after: String`, `first: Int`, `last: Int`, `q: String`, `orderBy: String`, `category: String`, `feed: String`, `mediaId: String` | `tacks` | `tacks`, `edges`, `cursor`, `node`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `totalCount` | `graphql-BRj5a0xt.js` |
| `listTaskSummaries` | `before: String`, `after: String`, `first: Int`, `last: Int`, `userId: ID!`, `status: String`, `keyword: String`, `createdAt: DateRange` | `taskSummaries` | `taskSummaries`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `edges`, `node` | `graphql-BRj5a0xt.js` |
| `listUserActiveDecorations` | `id: ID`, `type: DecorationType` | `user` | `user`, `id`, `activeDecorations` | `graphql-BRj5a0xt.js` |
| `listUserCardSetProgress` | `userId: ID!`, `before: String`, `after: String`, `first: Int`, `last: Int`, `orderBy: String` | `user` | `user`, `id`, `collectionCardSetProgresses`, `edges`, `node`, `collectionCardSet`, `totalCollectionCards`, `ownedCollectionCards`, `pageInfo`, `hasNextPage` | `graphql-BRj5a0xt.js` |
| `listUserCollectionCards` | `userId: ID`, `type: CollectionCardType`, `rarity: CollectionCardRarity`, `collectionCardSetId: ID`, `before: String`, `after: String`, `first: Int`, `last: Int`, `orderBy: String` | `user` | `user`, `id`, `collectionCards`, `edges`, `node`, `userId`, `collectionCardId`, `serialNumber`, `obtainedFrom`, `collectionCard` | `graphql-BRj5a0xt.js` |
| `listUserDecorations` | `id: ID`, `before: String`, `after: String`, `first: Int`, `last: Int`, `type: DecorationType`, `codes: [String!]` | `user` | `user`, `id`, `decorations`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor` | `graphql-BRj5a0xt.js` |
| `listUserFollowers` | `userId: ID!`, `before: String`, `after: String`, `first: Int`, `last: Int` | `user` | `user`, `id`, `followers`, `edges`, `node`, `profiles`, `blockStatus`, `followerCount`, `cursor`, `pageInfo` | `graphql-BRj5a0xt.js` |
| `listUserFollowings` | `userId: ID!`, `private: Boolean`, `before: String`, `after: String`, `first: Int`, `last: Int` | `user` | `user`, `id`, `followings`, `edges`, `node`, `profiles`, `blockStatus`, `followerCount`, `cursor`, `pageInfo` | `graphql-BRj5a0xt.js` |
| `listUserLikedArtworks` | `userId: ID!`, `before: String`, `after: String`, `first: Int`, `last: Int`, `types: [ArtworkType!]`, `tackLanguage: String` | `user` | `user`, `id`, `likedArtworks`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor` | `graphql-BRj5a0xt.js` |
| `listUserLikedGenerationModel` | `userId: ID!`, `before: String`, `after: String`, `first: Int`, `last: Int`, `isNsfw: Boolean`, `types: [GenerationModelType!]` | `user` | `user`, `id`, `likedGenerationModelList`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor` | `graphql-BRj5a0xt.js` |
| `listUserQuotaLogs` | `userId: ID!`, `reason: String`, `currency: String`, `before: String`, `after: String`, `first: Int`, `last: Int` | `user` | `user`, `id`, `quotaLogs`, `totalCount`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `edges` | `graphql-BRj5a0xt.js` |
| `listUsers` | `before: String`, `after: String`, `first: Int`, `last: Int`, `feed: String`, `keyword: String` | `users` | `users`, `edges`, `node`, `cursor`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `totalCount` | `graphql-BRj5a0xt.js` |
| `listUserTasks` | `before: String`, `after: String`, `first: Int`, `last: Int`, `userId: ID!`, `status: String`, `keyword: String`, `sceneIds: [String!]`, `createdAt: DateRange`, `parameterFields: [String!]`, `workflowId: String`, `workflowVersionId: String` | `tasks` | `tasks`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `edges`, `node` | `graphql-BRj5a0xt.js` |
| `listUserTasksTyped` | `before: String`, `after: String`, `first: Int`, `last: Int`, `userId: ID!`, `status: String`, `keyword: String`, `sceneIds: [String!]`, `createdAt: DateRange`, `workflowId: String`, `workflowVersionId: String`, `modelId: ID` | `tasks` | `tasks`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `edges`, `node` | `graphql-BRj5a0xt.js` |
| `listUserTaskSummaries` | `userId: ID!`, `before: String`, `after: String`, `first: Int`, `last: Int`, `status: String`, `parameterFields: [String!]` | `user` | `user`, `id`, `taskSummaries`, `pageInfo`, `hasNextPage`, `hasPreviousPage`, `endCursor`, `startCursor`, `edges`, `node` | `graphql-BRj5a0xt.js` |
### subscription

| operation | variables | root field | fields… | chunk |
|---|---|---|---|---|
| `subscribeGeneratorPreviewEvents` | — | `generatorPreviewEvents` | `generatorPreviewEvents`, `generationPreview`, `taskId`, `images` | `graphql-BRj5a0xt.js` |
| `subscribePersonalEvents` | — | `personalEvents` | `personalEvents` | `graphql-BRj5a0xt.js` |
| `subscribeWorkflowEvents` | `taskId: ID!` | `workflowProgress` | `workflowProgress` | `graphql-BRj5a0xt.js` |
