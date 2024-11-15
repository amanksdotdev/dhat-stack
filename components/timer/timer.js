(() => {
    document.addEventListener("alpine:init", () => {
        Alpine.data("timer", () => ({
            timer: 0,
            started: false,
            interval: null,
            startTimer() {
                console.log(this)
                this.started = true;
                this.interval = setInterval(() => {
                    this.timer++;
                }, 1000);
            },
            stopTimer() {
                console.log(this)
                this.started = false;
                clearInterval(this.interval);
            }
        }))
    })
})();
