import { useQuery } from "@tanstack/react-query";
import { fetch } from "@marzneshin/common/utils";
import type { NotificationType } from "../types";

export async function fetchNotification({
    queryKey,
}: { queryKey: [string, number] }): Promise<NotificationType> {
    return await fetch(`/notifications/${queryKey[1]}`).then(result => {
        return {
            ...result,
            users: result.user_ids,
        };
    });
}

const NotificationQueryFetchKey = "notification-fetch-key";

export const useNotificationQuery = ({ notificationId }: { notificationId: number }) => {
    return useQuery({
        queryKey: [NotificationQueryFetchKey, notificationId],
        queryFn: fetchNotification,
        initialData: null,
    });
};
