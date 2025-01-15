import { fetch } from "@marzneshin/common/utils";
import { NotificationType } from "../types";
import {
    EntityQueryKeyType,
    FetchEntityReturn,
    UseEntityQueryProps
} from "@marzneshin/libs/entity-table";
import { useQuery } from "@tanstack/react-query";

export async function fetchNotifications({ queryKey }: EntityQueryKeyType): FetchEntityReturn<NotificationType> {
    const pagination = queryKey[1];
    const primaryFilter = queryKey[2];
    const filters = queryKey[4].filters;
    return fetch(`/notifications`, {
        query: {
            ...pagination,
            ...filters,
            label: primaryFilter,
            descending: queryKey[3].desc,
            order_by: queryKey[3].sortBy,
        }
    }).then((result) => {
        const notifications: NotificationType[] = result.items;
        return {
            entities: notifications,
            pageCount: result.pages
        };
    });
}


export const NotificationsQueryFetchKey = "notifications-fetch-key";

export const useNotificationsQuery = ({
    page, size, sortBy = "created_at", desc = false, filters = {}
}: UseEntityQueryProps) => {
    return useQuery({
        queryKey: [NotificationsQueryFetchKey, { page, size }, filters?.label ?? "", { sortBy, desc }, { filters }],
        queryFn: fetchNotifications,
        initialData: { entities: [], pageCount: 0 }
    })
}
