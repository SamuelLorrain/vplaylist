
export type AnalyticEvent = {
    type: "play"|"pause"|"seek"|"timeupdate"|"ended";
    value: number,
    timestamp: number
};

export class Analytics {
    uuid: string;
    events: AnalyticEvent[]

    constructor(uuid: string) {
      this.uuid = uuid;
      this.events = [];
    }

    updateAnalysis({type, value} : {type: "play"|"pause"|"seek"|"timeupdate"|"ended", value: number}) {
      this.events.push({
          type,
          value,
          timestamp: Math.floor(Date.now()/1000)
      })
    }

    debug() {
      console.log({
          uuid : this.uuid,
          events : this.events
      })
    }

    send() {
      if (this.events.length <= 5) {
          return;
      }
      this.updateAnalysis({type: "ended", value: -1})
      fetch(`http://localhost:8000/video/${this.uuid}/analytics`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            timestamp: Math.floor(Date.now()/1000),
            events: this.events.map((i) => {
                return {
                    event_type: i.type,
                    value: i.value,
                    timestamp: i.timestamp
                }
            })
        })
      })
      .then(res => {
          if (res.status >= 400) {
              throw Error("Analytics failed");
          }
      })
    }
}
