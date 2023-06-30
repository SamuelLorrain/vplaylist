"use client";

import Toolbar from '@/components/Toolbar';
import VideoPlayer from '@/components/VideoPlayer';
import Playlist from '@/components/Playlist';
import VideoDetails from '@/components/VideoDetails';
import RouteGuard from '@/components/RouteGuard';

export default function Player() {
    return (
        <RouteGuard>
          <div className="mb-5">
            <Toolbar/>
            <div className="flex px-20 gap-5">
              <div className="w-2/3">
                <VideoPlayer/>
                <VideoDetails/>
              </div>
              <div className="w-1/3">
                <Playlist/>
              </div>
            </div>
          </div>
       </RouteGuard>
    );
}
