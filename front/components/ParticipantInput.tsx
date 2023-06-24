import React, { useState, useEffect } from 'react';
import debounce from 'lodash/debounce';
import {
    DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent
} from '@/components/ui/dropdown-menu';
import { Separator } from '@/components/ui/separator';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { XCircle } from 'lucide-react';
import { globalKeydownEventIsCancelled } from '@/contexts/recoilState';
import { useSetRecoilState } from 'recoil';
import {
    Skeleton
} from '@/components/ui/skeleton';

type MediaDetailElementType = {
    uuid: string,
    name: string,
    tags?: string[],
    note?: number
}

type TagInputType = {
    uuid: string;
    resource: string;
    initialValues: MediaDetailElementType[];
};

const searchParticipant = debounce(async function(value: string, resource: string, setter: Function, setIsLoading: Function) {
    const urlString = `${process.env.NEXT_PUBLIC_BACK_HOST}/${resource}`
    const url = new URL(urlString)
    url.searchParams.set('search', value);
    const response = await fetch(url.toString());
    if (response.status >= 400) {
        throw new Error(`unable to search for ${resource}`);
    }
    const values: MediaDetailElementType[] = (await response.json());
    setter(values);
    setIsLoading(false);
}, 1000);

const addNewParticipant = async (name: string, resource: string) => {
    const url = `${process.env.NEXT_PUBLIC_BACK_HOST}/${resource}`;
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name
        })
    });
    if (response.status >= 400) {
        throw new Error(`Unable to add new ${resource}`);
    }
    return response.json();
};

const addParticipantRelation = async (video_uuid: string, resource_uuid: string, resource: string) => {
    const url = `${process.env.NEXT_PUBLIC_BACK_HOST}/video/${video_uuid}/${resource}/${resource_uuid}`;
    const response = await fetch(url, {
        method: 'POST',
    });
    if (response.status >= 400) {
        throw new Error(`Unable to add new ${resource} relation`);
    }
    return response;
};

const removeParticipantRelation = async (video_uuid: string, resource_uuid: string, resource: string) => {
    const url = `${process.env.NEXT_PUBLIC_BACK_HOST}/video/${video_uuid}/${resource}/${resource_uuid}`;
    const response = await fetch(url, {
        method: 'DELETE',
    });
    if (response.status >= 400) {
        throw new Error(`Unable to remove ${resource}`);
    }
    return response;
};

export const ParticipantInput = ({uuid, resource, initialValues}: TagInputType) => {
    const [newValue, setNewValue] = useState<string>('');
    const [values, setValues] = useState<MediaDetailElementType[]>([]);
    const [searchValues, setSearchValues] = useState<MediaDetailElementType[]>([]);
    const [isLoadingSearch, setIsLoadingSearch] = useState<boolean>();
    const setIsCancelledKeydownEvent = useSetRecoilState(globalKeydownEventIsCancelled);

    useEffect(() => {
        setValues([...initialValues]);
    }, [initialValues]);

    return (
      <div className="flex h-10 border border-input cursor-pointer rounded-s">
        {
          values.map((value) => {
            return <div key={"chip-" + value.name} className="ml-2 my-1 px-2 border rounded-md bg-secondary/80 cursor-auto flex justify-center items-center">
                <div>{value.name}</div>
                <div className="cursor-pointer ml-1" onClick={() => {
                  setValues(existingValues => {
                    return existingValues.filter((existingValue) => {
                      return existingValue.name != value.name;
                    })
                  })
                  removeParticipantRelation(uuid, value.uuid, resource)
                  .catch(() => {
                    setValues(existingValues => [...existingValues, value])
                  })
                }
                }>
                    <XCircle size={16} strokeWidth={1.25}/>
                </div>
            </div>
          })
        }
        <DropdownMenu onOpenChange={(open) => setIsCancelledKeydownEvent(open)}>
          <DropdownMenuTrigger asChild>
            <div className="ml-2 pl-100 grow"></div>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="start">
              <div className="flex gap-2">
                <Input
                    type="text"
                    aria-label="searching new participant"
                    placeholder="type new participant here"
                    value={newValue}
                    onChange={(e) => {
                            setNewValue(e.target.value);
                            if (e.target.value === '' || e.target.value == null) {
                                setSearchValues([]);
                                return;
                            }
                            setIsLoadingSearch(true);
                            searchParticipant(e.target.value, resource, setSearchValues, setIsLoadingSearch);
                        }
                    }
                />
              </div>
              {
                  searchValues.length !== 0 &&
                  <Separator className="my-2"/>
              }
              {
                isLoadingSearch ?
                <div>
                    <Separator className="my-2"/>
                    <Skeleton className="p-2 h-10 w-100"/>
                </div>
                :
                searchValues.map((v) => {
                    return <div key={"dropdown-" + v.name}
                                className="cursor-pointer"
                                onClick={() => {
                                        setValues(values => [...values, v]);
                                        addParticipantRelation(uuid, v.uuid, resource)
                                        .catch(() => {
                                            setValues(values => values.filter(x => {
                                                return x.name != v.name
                                            }));
                                        })
                                    }
                                }
                            >
                        {v.name}
                    </div>;
                })
              }
              {
                searchValues.length <= 0 && !isLoadingSearch && newValue.length > 0 &&
                (
                 <>
                   <Separator className="my-2"/>
                   <div className="flex justify-center mt-2">
                     <Button onClick={() => {
                        addNewParticipant(newValue, resource)
                        .then(value => {
                            setValues(values => [...values, value]);
                            setNewValue("");
                            addParticipantRelation(uuid, value.uuid, resource)
                            .catch(() => {
                                setValues(values => values.filter(x => {
                                    return x.name != value.name
                                }));
                            })
                        })
                     }}>Add</Button>
                   </div>
                 </>
                )
              }
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    );
}

export default ParticipantInput;
