import { Switch, FormField, FormControl, FormItem, FormLabel } from "@marzneshin/common/components";
import { useTranslation } from "react-i18next";
import { useFormContext } from "react-hook-form";

export const IsPublic = () => {
    const form = useFormContext();
    const { t } = useTranslation();
    return (
        <FormField
            control={form.control}
            name="is_public"
            render={({ field }) => (
                <FormItem>
                    <FormLabel>{t("is_public")}</FormLabel>
                    <FormControl>
                        <Switch
                            {...field}
                            checked={field.value}
                            onCheckedChange={field.onChange}
                        />
                    </FormControl>
                </FormItem>
            )}
        />
    )
}
