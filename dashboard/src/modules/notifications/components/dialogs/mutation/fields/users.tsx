import {
    FormItem,
    FormControl,
    FormMessage,
    FormLabel,
    FormField,
    Checkbox,
    ScrollArea,
    EntityFieldCard,
} from "@marzneshin/common/components";
import {
    useFormContext,
    type FieldValues,
    type ControllerRenderProps,
} from "react-hook-form";
import { useTranslation } from "react-i18next";
import { cn } from "@marzneshin/common/utils";
import { UserCircleIcon, CheckCircleIcon } from "lucide-react";
import { UserType, useUsersQuery } from "@marzneshin/modules/users";

export const UserCard = ({
    user,
    field,
}: {
    user: UserType;
    field: ControllerRenderProps<FieldValues, "user_ids">;
}) => {
    return (
        <div
            className={cn(
                "flex flex-row items-center p-3 space-y-0 space-x-3 rounded-md border",
                {
                    "bg-secondary": field.value?.includes(user.id),
                },
            )}
        >
            <Checkbox
                checked={field.value?.includes(user.id)}
                onCheckedChange={(checked) => {
                    return checked
                        ? field.onChange([...field.value, user.id])
                        : field.onChange(
                            field.value?.filter((value: number) => value !== user.id),
                        );
                }}
            />
            <FormLabel className="flex flex-row justify-between items-center w-full">
                <EntityFieldCard
                    FirstIcon={UserCircleIcon}
                    SecondIcon={CheckCircleIcon}
                    firstAmount={user.id}
                    secondAmount={user.is_active ? "Active" : "Inactive"}
                    name={user.username}
                />
            </FormLabel>
        </div>
    );
};

export const UsersField = () => {
    const { data } = useUsersQuery({ page: 1, size: 100 });
    const form = useFormContext();
    const { t } = useTranslation();

    return (
        <FormField
            control={form.control}
            name="user_ids"
            render={() => (
                <FormItem>
                    <FormLabel>{t("users")}</FormLabel>
                    <ScrollArea className="flex flex-col justify-start  h-full max-h-[20rem]">
                        {data.entities.map((user) => (
                            <FormField
                                key={user.id}
                                control={form.control}
                                name="user_ids"
                                render={({ field }) => (
                                    <FormItem key={user.id} className="mb-1">
                                        <FormControl>
                                            <UserCard user={user} field={field} />
                                        </FormControl>
                                    </FormItem>
                                )}
                            />
                        ))}
                    </ScrollArea>
                    <FormMessage />
                </FormItem>
            )}
        />
    );
};
