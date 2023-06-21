
export type AnalyticEvent = {
    type: "play"|"pause"|"seek"|"timeupdate"|"ended";
    currentTime: number,
};

export class Analytics {
    uuid: string;
    totalDuration: number
    events: AnalyticEvent[]

    constructor(uuid: string) {
      this.uuid = uuid;
      this.totalDuration = -1;
      this.events = [];
    }

    setTotalDuration(totalDuration: number) {
      this.totalDuration = totalDuration;
    }

    updateAnalysis({type, currentTime} : AnalyticEvent) {
      this.events.push({
          type,
          currentTime
      })
    }

    debug() {
      console.log({
          uuid : this.uuid,
          totalDuration : this.totalDuration,
          events : this.events
      })
    }

    send() {
      if (this.events.length <= 5) {
          return;
      }
    }
}

