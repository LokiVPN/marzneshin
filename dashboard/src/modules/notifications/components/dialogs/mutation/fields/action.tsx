import {
    FormControl,
    FormField,
    FormItem,
    Select,
    SelectTrigger,
    SelectValue,
    SelectContent,
    SelectItem,
    FormLabel,
    FormMessage,
    FormDescription,
} from "@marzneshin/common/components";
import type { FC, InputHTMLAttributes } from "react";
import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

export const ActionField: FC<InputHTMLAttributes<HTMLElement>> = ({
    disabled,
}) => {
    const form = useFormContext();
    const { t } = useTranslation();

    return (
        <FormField
            control={form.control}
            name="action"
            render={({ field }) => (
                <FormItem className="w-full">
                    <FormLabel>{t("page.notifications.action")}</FormLabel>
                    <Select
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                        disabled={disabled}
                    >
                        <FormControl>
                            <SelectTrigger>
                                <SelectValue placeholder="Notification action" />
                            </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                            <SelectItem value="user_created">User created</SelectItem>
                            <SelectItem value="user_updated">User updated</SelectItem>
                            <SelectItem value="user_activated">User activated</SelectItem>
                            <SelectItem value="user_deactivated">User deactivated</SelectItem>
                            <SelectItem value="user_deleted">User deleted</SelectItem>
                            <SelectItem value="user_enabled">User enabled</SelectItem>
                            <SelectItem value="user_disabled">User disabled</SelectItem>
                            <SelectItem value="data_usage_reset">Data usage reset</SelectItem>
                            <SelectItem value="subscription_revoked">Subscription revoked</SelectItem>
                            <SelectItem value="reached_usage_percent">Reached usage percent</SelectItem>
                            <SelectItem value="reached_days_left">Reached days left</SelectItem>
                            <SelectItem value="get_bonus">Get bonus</SelectItem>
                            <SelectItem value="custom">Custom</SelectItem>
                        </SelectContent>
                    </Select>
                    <FormDescription>
                        {t("page.notifications.action_desc")}
                    </FormDescription>
                    <FormMessage />
                </FormItem>
            )}
        />
    );
};