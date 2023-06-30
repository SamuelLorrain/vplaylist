import React, { useCallback, useState } from 'react';
import debounce from 'lodash/debounce';
import { useRecoilValue } from 'recoil';
import { authenticationToken } from '@/contexts/recoilState';
import { Input } from '@/components/ui/input';

type UpdateInputType = {
    value: string;
    className?: string;
    uuid: string;
    type: string;
    updatedValue: string;
    formatter?: (x: any) => string;
};

const UpdateInput = ({value, uuid, type, updatedValue, className, formatter}: UpdateInputType) => {
    const [displayedValue, setDisplayedValue] = useState<string|undefined>(value);
    const [isPending, setIsPending] = useState(false);
    const authenticationTokenValue = useRecoilValue(authenticationToken);

    function updateDisplayName(oldValue: string|undefined, newValue: string) {
        const formatted = formatter ? formatter(newValue) : newValue;
        fetch(`${process.env.NEXT_PUBLIC_BACK_HOST}/video/${uuid}/details`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + authenticationTokenValue
            },
            body: JSON.stringify({
                [updatedValue]: formatted,
            })
        })
        .then(response => {
            if(response.status >= 400) {
                throw Error();
            }
        })
        .catch(() => {
            setDisplayedValue(oldValue);
        })
        .finally(() => {
            setIsPending(false);
        });
    }

    const debounceUpdate =
        useCallback(
            debounce(updateDisplayName,
            1500
        ), [uuid]);

    return (
        <div>
            <Input className={className}
                type={type}
                value={displayedValue ?? ''}
                onChange={(e) => {
                  setDisplayedValue(e.target.value);
                  setIsPending(true);
                  debounceUpdate(displayedValue, e.target.value);
                }}
                />
            {isPending ? 'is pending': ''}
        </div>
    );
}

export default UpdateInput;
