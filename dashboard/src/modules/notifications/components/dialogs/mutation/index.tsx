import {
    DialogTitle,
    DialogContent,
    Dialog,
    DialogHeader,
    Form,
    Button,
} from "@marzneshin/common/components";
import { type FC, useMemo } from "react";
import {
    type NotificationType,
    useNotificationsCreationMutation,
    useNotificationsUpdateMutation,
    NotificationAction,
    NotificationEditSchema,
    NotificationCreateSchema
} from "@marzneshin/modules/notifications";
import { useTranslation } from "react-i18next";
import { useMutationDialog, MutationDialogProps } from "@marzneshin/common/hooks";
import { ActionField, LabelField, MessageField, UsersField } from "./fields";


export const MutationDialog: FC<MutationDialogProps<NotificationType>> = ({
    entity,
    onClose,
}) => {
    const defaultValue = useMemo(() => ({
        label: "",
        message: "",
        action: NotificationAction.CUSTOM,
        user_ids: [],
    }), []);
    const updateMutation = useNotificationsUpdateMutation();
    const createMutation = useNotificationsCreationMutation();
    const { open, onOpenChange, form, handleSubmit } = useMutationDialog({
        onClose,
        entity,
        updateMutation,
        createMutation,
        defaultValue,
        schema: entity ? NotificationEditSchema : NotificationCreateSchema,
    });
    const { t } = useTranslation();

    return (
        <Dialog open={open} onOpenChange={onOpenChange} defaultOpen={true}>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle className="text-primary">
                        {entity
                            ? t("page.notifications.dialogs.edition.title")
                            : t("page.notifications.dialogs.creation.title")}
                    </DialogTitle>
                </DialogHeader>
                <Form {...form}>
                    <form onSubmit={handleSubmit} className="h-full">
                        <LabelField disabled={!!entity} />
                        <ActionField disabled={!!entity} />
                        <MessageField />
                        <UsersField />
                        <Button
                            className="mt-3 w-full font-semibold"
                            type="submit"
                            disabled={form.formState.isSubmitting}
                        >
                            {t("submit")}
                        </Button>
                    </form>
                </Form>
            </DialogContent>
        </Dialog>
    );
};
