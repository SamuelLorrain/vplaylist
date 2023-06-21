import React, { useCallback, useState } from 'react';
import debounce from 'lodash/debounce';

type UpdateInputType = {
    value: string;
    uuid: string;
    type: string;
    updatedValue: string;
    formatter?: (x: any) => string;
};

const UpdateInput = ({value, uuid, type, updatedValue, formatter}: UpdateInputType) => {
    const [displayedValue, setDisplayedValue] = useState<string|undefined>(value);
    const [isPending, setIsPending] = useState(false);

    function updateDisplayName(oldValue: string|undefined, newValue: string) {
        const formatted = formatter ? formatter(newValue) : newValue;
        fetch(`http://localhost:8000/video/${uuid}/details`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
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
        <span>
            <input
                type={type}
                value={displayedValue ?? ''}
                onChange={(e) => {
                  setDisplayedValue(e.target.value);
                  setIsPending(true);
                  debounceUpdate(displayedValue, e.target.value);
                }}
                />
            {isPending ? 'is pending': ''}
        </span>
    );
}

export default UpdateInput;
