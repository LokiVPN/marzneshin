import {
    type UserType,
    OnlineStatus,
    UserUsedTraffic,
    UserActivatedPill,
    UserExpireStrategyPill,
    UserExpirationValue
} from "@marzneshin/modules/users";
import i18n from "@marzneshin/features/i18n";
import {
    CopyToClipboardButton,
    buttonVariants,
    NoPropogationButton,
} from "@marzneshin/common/components";
import { LinkIcon } from "lucide-react";
import { getSubscriptionLink } from "@marzneshin/common/utils";
import {
    DataTableColumnHeader,
    DataTableActionsCell,
    type ColumnActions, type ColumnDefWithSudoRole
} from "@marzneshin/libs/entity-table";

export const columns = (actions: ColumnActions<UserType>): ColumnDefWithSudoRole<UserType>[] => [
    {
        accessorKey: "id",
        header: ({ column }) => (
            <DataTableColumnHeader title={i18n.t("telegram_id")} column={column} />
        ),
        cell: ({ row }) => (
            <div className="flex flex-row gap-2 items-center">
                <OnlineStatus user={row.original} /> {row.original.id}
            </div>
        ),
    },
    {
        accessorKey: "username",
        header: ({ column }) => (
            <DataTableColumnHeader title={i18n.t("username")} column={column} />
        ),
    },
    {
        accessorKey: "activated",
        enableSorting: false,
        header: ({ column }) => (
            <DataTableColumnHeader
                title={i18n.t("activated")}
                column={column}
            />
        ),
        cell: ({ row }) => <UserActivatedPill user={row.original} />,
    },
    {
        accessorKey: "used_traffic",
        header: ({ column }) => (
            <DataTableColumnHeader
                title={i18n.t("page.users.used_traffic")}
                column={column}
            />
        ),
        cell: ({ row }) => <UserUsedTraffic user={row.original} />,
    },
    {
        accessorKey: "expire_strategy",
        header: ({ column }) => (
            <DataTableColumnHeader
                title={i18n.t("page.users.expire_method")}
                column={column}
            />
        ),
        cell: ({ row }) => <UserExpireStrategyPill user={row.original} />,
        enableSorting: false,
    },
    {
        accessorKey: "expire_date",
        header: ({ column }) => (
            <DataTableColumnHeader
                title={i18n.t("page.users.expire_date")}
                column={column}
            />
        ),
        cell: ({ row }) => <UserExpirationValue user={row.original} />,
    },
    {
        id: "actions",
        cell: ({ row }) => (
            <NoPropogationButton row={row} actions={actions}>
                <CopyToClipboardButton
                    text={getSubscriptionLink(row.original.subscription_url)}
                    successMessage={i18n.t(
                        "page.users.settings.subscription_link.copied",
                    )}
                    copyIcon={LinkIcon}
                    className={buttonVariants({
                        variant: "secondary",
                        className: "size-8",
                    })}
                    tooltipMsg={i18n.t("page.users.settings.subscription_link.copy")}
                />
                <DataTableActionsCell {...actions} row={row} />
            </NoPropogationButton>
        )
    }
];

