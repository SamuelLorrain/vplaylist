import { useVideoDetails } from '@/hooks/videoDetails';
import React from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { useRecoilState } from 'recoil';
import { currentPlaylistElement, openVideoDetails, autodiscoveryMode } from '@/contexts/recoilState';
import UpdateInput from './UpdateInput';
import TagInput from './TagInput';
import { twMerge } from 'tailwind-merge';

const VideoDetails: React.FC = () => {
    const [autoDiscoveryModeState, setAutoDiscoveryModeState] = useRecoilState(autodiscoveryMode);
    const [currentPlaylistElementState] = useRecoilState(currentPlaylistElement);
    const [open, setOpen] = useRecoilState(openVideoDetails);
    const { data, error } = useVideoDetails(currentPlaylistElementState.uuid);

    if (error) {
        return "error";
    }
    if (data) {
        return (
        <Collapsible open={open}>
          <CollapsibleTrigger asChild>
              <div className={twMerge("p-2 flex justify-between cursor-pointer border-x", !open && "border rounded-b-md")}
                   onClick={() => setOpen(open => !open)}>
                  <h2>{data.path ?? data.name ?? data.uuid}</h2>
                  <div className="grow flex justify-end items-center gap-2 mr-5">
                    <Label htmlFor="auto-discovery-id">Auto discovery</Label>
                    <Switch id="auto-discovery-id"
                            checked={autoDiscoveryModeState}
                            onCheckedChange={() =>
                                setAutoDiscoveryModeState((check: boolean) => !check)
                            }
                    />
                  </div>
                  {
                      open  ? <ChevronUp/> : <ChevronDown/>
                  }
              </div>
          </CollapsibleTrigger>
          <CollapsibleContent asChild>
            <div className="border-x p-2 border-b rounded-b-md">
              <div className="flex flex-col gap-2">
                <div>
                    <Label>name</Label>
                    <UpdateInput type="text" value={data ? data.name : ''} uuid={currentPlaylistElementState.uuid} updatedValue="name"/>
                </div>
                <div>
                    <Label>participants</Label>
                    <TagInput
                        initialValues={data?.participants ?? []}
                        resource="participant"
                        uuid={currentPlaylistElementState.uuid}/>
                </div>
                <div>
                    <Label>tags</Label>
                    <TagInput
                        initialValues={data?.tags ?? []}
                        resource="tag"
                        uuid={currentPlaylistElementState.uuid}/>
                </div>
                <div>
                    <Label>date_down</Label>
                    <UpdateInput type="date"
                                 value={data ? data.date_down : new Date()}
                                 uuid={currentPlaylistElementState.uuid}
                                 updatedValue="date_down"
                                 className="w-auto"
                                 formatter={(x) => {
                                    const d = new Date(x);
                                    return `${d.getDay()}-${d.getMonth()}-${d.getFullYear()}`
                                 }}/>
                </div>
                <div>
                    <Label>note</Label>
                    <UpdateInput type="number" value={data ? data.note: ''} uuid={currentPlaylistElementState.uuid} updatedValue="note"/>
                </div>
              </div>
            </div>
          </CollapsibleContent>
        </Collapsible>);
    }
    return "loading..."
}

export default VideoDetails;
