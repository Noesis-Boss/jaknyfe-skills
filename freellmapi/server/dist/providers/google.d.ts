import type { ChatMessage, ChatCompletionResponse, ChatCompletionChunk } from '@freellmapi/shared/types.js';
import { BaseProvider, type CompletionOptions } from './base.js';
import { type QuotaObservationContext } from '../services/provider-quota.js';
export declare function sanitizeForGemini(schema: unknown): unknown;
export declare class GoogleProvider extends BaseProvider {
    readonly platform: "google";
    readonly name = "Google AI Studio";
    chatCompletion(apiKey: string, messages: ChatMessage[], modelId: string, options?: CompletionOptions, quotaContext?: QuotaObservationContext): Promise<ChatCompletionResponse>;
    streamChatCompletion(apiKey: string, messages: ChatMessage[], modelId: string, options?: CompletionOptions, quotaContext?: QuotaObservationContext): AsyncGenerator<ChatCompletionChunk>;
    validateKey(apiKey: string, quotaContext?: QuotaObservationContext): Promise<boolean>;
}
//# sourceMappingURL=google.d.ts.map