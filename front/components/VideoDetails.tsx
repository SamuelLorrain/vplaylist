import { useState } from 'react';
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

const VideoDetails: React.FC = () => {
    const [currentPlaylistElementState] = useRecoilState(currentPlaylistElement);
    const [open, setOpen] = useState(false);
    const { data, error } = useVideoDetails(currentPlaylistElementState.uuid);

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
                    <li>{data.name}</li>
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
