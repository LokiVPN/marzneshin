import { ColumnDef } from "@tanstack/react-table";
import { NotificationType } from "@marzneshin/modules/notifications";
import {
    DataTableActionsCell,
    DataTableColumnHeader
} from "@marzneshin/libs/entity-table"
import i18n from "@marzneshin/features/i18n";
import {
    NoPropogationButton,
} from "@marzneshin/common/components";
import { ColumnActions } from "@marzneshin/libs/entity-table";

export const columns = (actions: ColumnActions<NotificationType>): ColumnDef<NotificationType>[] => ([
    {
        accessorKey: "label",
        header: ({ column }) => <DataTableColumnHeader title={i18n.t('label')} column={column} />,
    },
    {
        accessorKey: "action",
        header: ({ column }) => <DataTableColumnHeader title={i18n.t('action')} column={column} />,
    },
    {
        accessorKey: "users",
        header: ({ column }) => <DataTableColumnHeader title={i18n.t('users')} column={column} />,
        cell: ({ row }) => `${row.original.user_ids.length}`
    },
    {
        id: "actions",
        cell: ({ row }) => {
            return (
                <NoPropogationButton row={row} actions={actions}>
                    <DataTableActionsCell {...actions} row={row} />
                </NoPropogationButton>
            );
        },
    }
]);
