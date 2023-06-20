import { useState, useEffect, useCallback } from 'react';
import { useVideoDetails } from '@/hooks/videoDetails';
import React from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import { useRecoilState } from 'recoil';
import { currentPlaylistElement } from '@/contexts/recoilState';
import debounce from 'lodash/debounce';

const VideoDetails: React.FC = () => {
    const [currentPlaylistElementState] = useRecoilState(currentPlaylistElement);
    const [open, setOpen] = useState(false);
    const { data, error } = useVideoDetails(currentPlaylistElementState.uuid);
    const [displayedName, setDisplayedName] = useState<string|undefined>(data?.name);
    const [isPending, setIsPending] = useState(false);

    useEffect(() => {
        if (data?.name) {
            setDisplayedName(data?.name);
        }
    }, [JSON.stringify(data)]);

    function updateDisplayName(oldValue: string|undefined, newValue: string) {
        fetch(`http://localhost:8000/video/${currentPlaylistElementState.uuid}/details`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: newValue
            })
        })
        .then(response => {
            if(response.status >= 400) {
                throw Error();
            }
        })
        .catch(() => {
            setDisplayedName(oldValue);
        })
        .finally(() => {
            setIsPending(false);
        });
    }

    const debounceUpdate = useCallback(debounce(updateDisplayName, 1500), [currentPlaylistElementState.uuid]);

    if (error) {
        return "error";
    }
    if (data) {
        return (
        <Collapsible>
          <CollapsibleContent asChild>
            <div className="border-x p-2">
                <ul>
                    <li>{data.uuid}</li>
                    <li>name : <input type="text"
                        value={displayedName}
                        onChange={(e) => {
                            setDisplayedName(e.target.value);
                            setIsPending(true);
                            debounceUpdate(displayedName, e.target.value);
                        }}
                    />
                        {isPending ? 'is pending': ''}
                        </li>
                    <li>{JSON.stringify(data.participants)}</li>
                    <li>{data.film}</li>
                    <li>{data.studio}</li>
                    <li>{JSON.stringify(data.tags)}</li>
                    <li>{data.date_down}</li>
                    <li>{data.note}</li>
                </ul>
            </div>
          </CollapsibleContent>
          <CollapsibleTrigger asChild>
              <div className="p-2 border rounded-b-md flex justify-between" onClick={() => setOpen(open => !open)}>
                  <h2>{data.path ?? data.name ?? data.uuid}</h2>
                  {
                      open  ? <ChevronUp/> : <ChevronDown/>
                  }
              </div>
          </CollapsibleTrigger>
        </Collapsible>
        );
    }
    return "loading..."
}

export default VideoDetails;
