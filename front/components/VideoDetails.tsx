import { useVideoDetails } from '@/hooks/videoDetails';
import React from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import { useRecoilState } from 'recoil';
import { currentPlaylistElement, openVideoDetails } from '@/contexts/recoilState';
import UpdateInput from './UpdateInput';

const VideoDetails: React.FC = () => {
    const [currentPlaylistElementState] = useRecoilState(currentPlaylistElement);
    const [open, setOpen] = useRecoilState(openVideoDetails);
    const { data, error } = useVideoDetails(currentPlaylistElementState.uuid);

    if (error) {
        return "error";
    }
    if (data) {
        return (
        <Collapsible open={open}>
          <CollapsibleContent asChild>
            <div className="border-x p-2">
              <ul>
                <li>name : <UpdateInput type="text" value={data ? data.name : ''} uuid={currentPlaylistElementState.uuid} updatedValue="name"/></li>
                <li>participants: {JSON.stringify(data.participants)}</li>
                <li>film : {data.film}</li>
                <li>studio : {data.studio}</li>
                <li>tags: {JSON.stringify(data.tags)}</li>
                <li>
                    date_down :
                    <UpdateInput type="date"
                                 value={data ? data.date_down : new Date()}
                                 uuid={currentPlaylistElementState.uuid}
                                 updatedValue="date_down"
                                 formatter={(x) => {
                                    const d = new Date(x);
                                    return `${d.getDay()}-${d.getMonth()}-${d.getFullYear()}`
                                 }}/>
                </li>
                <li>note : <UpdateInput type="number" value={data ? data.note: ''} uuid={currentPlaylistElementState.uuid} updatedValue="note"/></li>
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
        </Collapsible>);
    }
    return "loading..."
}

export default VideoDetails;
