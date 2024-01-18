function routeToSummary(button) {
    let title = encodeURIComponent(button.dataset.title);
    let paperType = button.dataset.paperType;
    
    let route;
    if (paperType === "NowPaper") {
        route = "/post_deepersummary/" + title;
    } else {
        route = "/deepersummary/" + title;
    }

    window.location.href = route;
}
