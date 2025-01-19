import { useQuery } from "@tanstack/react-query";
import { fetch } from "@marzneshin/common/utils";
import type { NotificationTargetType } from "@marzneshin/modules/notifications";
import type {
    DoubleEntityQueryKeyType,
    UseEntityQueryProps,
    FetchEntityReturn
} from "@marzneshin/libs/entity-table";

interface UseNotificationUsersQueryProps extends UseEntityQueryProps {
    notificationId: number;
}

export async function fetchNotificationUsers({ queryKey }: DoubleEntityQueryKeyType): FetchEntityReturn<NotificationTargetType> {
    const pagination = queryKey[2];
    const primaryFilter = queryKey[3];
    return fetch(`/notifications/${queryKey[1]}/users`, {
        query: {
            ...pagination,
            username: primaryFilter,
        }
    }).then((result) => {
        return {
            entities: result.items,
            pageCount: result.pages,
        };
    });
}

const NotificationsQueryFetchKey = "notifications-users-fetch-key";

export const useUsersNotificationQuery = ({
    notificationId, page = 1, size = 50
}: UseNotificationUsersQueryProps) => {
    return useQuery({
        queryKey: [NotificationsQueryFetchKey, notificationId, { page, size }],
        queryFn: fetchNotificationUsers,
        initialData: { entities: [], pageCount: 0 },
    })
}
