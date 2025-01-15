import {
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
    FormDescription,
} from "@marzneshin/common/components";
import type { FC, InputHTMLAttributes } from "react";
import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";
import MDEditor, { commands }  from '@uiw/react-md-editor/nohighlight';

export const MessageField: FC<InputHTMLAttributes<HTMLElement>> = () => {
    const form = useFormContext();
    const { t } = useTranslation();

    return (
        <FormField
            control={form.control}
            name="message"
            render={({ field }) => (
                <FormItem>
                    <FormLabel>{t("page.notifications.message")}</FormLabel>
                    <MDEditor
                        value={field.value}
                        onChange={field.onChange}
                        preview="edit"
                        commands={[
                            commands.bold,
                            commands.italic,
                            commands.link,
                            commands.quote,
                            commands.orderedListCommand
                        ]}
                        extraCommands={[
                            commands.codeEdit, commands.codePreview
                          ]}
                        style={{ whiteSpace: 'pre-wrap' }}
                    />
                    <FormDescription>
                        {t("page.notifications.message_desc")}
                    </FormDescription>
                    <FormMessage />
                </FormItem>
            )}
        />
    );
};