import { z } from "zod";

export const NotificationCreateSchema = z.object({
    id: z.number().optional(),
    label: z.string().trim().min(1).max(128),
    message: z.string().trim().min(1).max(1024),
    user_ids: z.array(z.number()),
    action: z.string().refine((value) => {
        return [
            "user_created",
            "user_updated",
            "user_activated",
            "user_deactivated",
            "user_deleted",
            "user_enabled",
            "user_disabled",
            "data_usage_reset",
            "subscription_revoked",
            "reached_usage_percent",
            "reached_days_left",
            "get_bonus",
            "custom",
        ].includes(value);
    }),
})

export const NotificationEditSchema = z.object({
    id: z.number(),
    message: z.string().trim().min(1).max(1024),
    user_ids: z.array(z.number()),
})

export type NotificationMutationType = z.infer<typeof NotificationCreateSchema>