function select() {
    $("li").on("click", function () {
        this.addClass("active");
        this.siblings().removeClass("active");
    })
}