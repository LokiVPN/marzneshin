import { NotificationMutationType, NotificationsQueryFetchKey } from "@marzneshin/modules/notifications";
import { useMutation } from "@tanstack/react-query";
import { fetch, queryClient } from "@marzneshin/common/utils";
import { toast } from "sonner";
import i18n from "@marzneshin/features/i18n";

export async function fetchCreateNotification(notification: NotificationMutationType): Promise<NotificationMutationType> {
    return fetch('/notifications', { method: 'post', body: notification }).then((notification) => {
        return notification;
    });
}

const handleError = (error: Error, value: NotificationMutationType) => {
    toast.error(
        i18n.t('events.create.error', { name: value.label }),
        {
            description: error.message
        })
}

const handleSuccess = (value: NotificationMutationType) => {
    toast.success(
        i18n.t('events.create.success.title', { name: value.label }),
        {
            description: i18n.t('events.create.success.desc')
        })
    queryClient.invalidateQueries({ queryKey: [NotificationsQueryFetchKey] })
}


const NotificationsCreateFetchKey = "notifications-create-fetch-key";

export const useNotificationsCreationMutation = () => {
    return useMutation({
        mutationKey: [NotificationsCreateFetchKey],
        mutationFn: fetchCreateNotification,
        onError: handleError,
        onSuccess: handleSuccess,
    })
}
