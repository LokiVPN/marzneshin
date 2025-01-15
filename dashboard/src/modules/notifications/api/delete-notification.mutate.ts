import { NotificationType, NotificationsQueryFetchKey } from "@marzneshin/modules/notifications";
import { useMutation } from "@tanstack/react-query";
import { fetch, queryClient } from "@marzneshin/common/utils";
import { toast } from "sonner";
import i18n from "@marzneshin/features/i18n";

export async function fetchDeleteNotification(notification: NotificationType): Promise<NotificationType> {
    return fetch(`/notifications/${notification.id}`, { method: 'delete' }).then((notification) => {
        return notification;
    });
}

const NotificationsDeleteFetchKey = "notifications-delete-fetch-key";


const handleError = (error: Error, value: NotificationType) => {
    toast.error(
        i18n.t('events.delete.error', { name: value.label }),
        {
            description: error.message
        })
}

const handleSuccess = (value: NotificationType) => {
    toast.success(
        i18n.t('events.delete.success.title', { name: value.label }),
        {
            description: i18n.t('events.delete.success.desc')
        })
    queryClient.invalidateQueries({ queryKey: [NotificationsQueryFetchKey] })
}

export const useNotificationsDeletionMutation = () => {
    return useMutation({
        mutationKey: [NotificationsDeleteFetchKey],
        mutationFn: fetchDeleteNotification,
        onError: handleError,
        onSuccess: handleSuccess,
    })
}
