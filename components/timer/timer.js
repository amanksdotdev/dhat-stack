(() => {
    document.addEventListener("alpine:init", () => {
        Alpine.data("timer", () => ({
            timer: 0,
            started: false,
            interval: null,
            startTimer() {
                this.started = true;
                this.interval = setInterval(() => {
                    this.timer++;
                }, 1000);
            },
            stopTimer() {
                this.started = false;
                clearInterval(this.interval);
            }
        }))
    })
})();
