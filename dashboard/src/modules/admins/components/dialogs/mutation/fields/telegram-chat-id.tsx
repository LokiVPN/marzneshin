import {
    FormControl,
    FormField,
    FormItem,
    Input,
    FormLabel,
    FormMessage,
} from "@marzneshin/common/components";
import type { FC, InputHTMLAttributes } from "react";
import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

export const TelegramChatIdField: FC<InputHTMLAttributes<HTMLElement>> = () => {
    const form = useFormContext();
    const { t } = useTranslation();

    const updateFieldValue = (path: string, value: any) => {
        form.setValue(path, value === "" ? null : value, {
            shouldDirty: true,
            shouldValidate: true,
        });
    };

    return (
        <FormField
            control={form.control}
            name="telegram_chat_id"
            render={({ field }) => (
                <FormItem>
                    <FormLabel>{t("telegram_chat_id")}</FormLabel>
                    <FormControl>
                        <Input
                            value={
                                field.value
                            }
                            type="number"
                            onChange={(e) =>
                                updateFieldValue(
                                    'telegram_chat_id',
                                    e.target
                                        .value ===
                                        ""
                                        ? null
                                        : Number.parseInt(
                                            e
                                                .target
                                                .value,
                                        ),
                                )
                            } />
                    </FormControl>
                    <FormMessage />
                </FormItem>
            )}
        />
    );
}