import type { FC } from "react";
import {
    NotificationsQueryFetchKey,
    fetchNotifications,
    NotificationType
} from "@marzneshin/modules/notifications";
import { columns as columnsFn } from "./columns";
import { EntityTable } from "@marzneshin/libs/entity-table";
import { useNavigate } from "@tanstack/react-router";

export const NotificationsTable: FC = () => {
    const navigate = useNavigate({ from: "/notifications" });
    const onEdit = (entity: NotificationType) => {
        navigate({
            to: "/notifications/$notificationId/edit",
            params: { notificationId: String(entity.id) },
        })
    }

    const onDelete = (entity: NotificationType) => {
        navigate({
            to: "/notifications/$notificationId/delete",
            params: { notificationId: String(entity.id) },
        })
    }

    const onOpen = (entity: NotificationType) => {
        navigate({
            to: "/notifications/$notificationId",
            params: { notificationId: String(entity.id) },
        })
    }

    const columns = columnsFn({ onEdit, onDelete, onOpen });

    return (
        <EntityTable
            fetchEntity={fetchNotifications}
            columns={columns}
            primaryFilter="label"
            entityKey={NotificationsQueryFetchKey}
            onCreate={() => navigate({ to: "/notifications/create" })}
            onOpen={onOpen}
        />
    );
};
