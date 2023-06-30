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
            <div className="lg:flex lg:px-5 xl:px-20 gap-5">
              <div className="lg:w-2/3">
                <VideoPlayer/>
                <VideoDetails/>
              </div>
              <div className="lg:w-1/3">
                <Playlist/>
              </div>
            </div>
          </div>
       </RouteGuard>
    );
}
