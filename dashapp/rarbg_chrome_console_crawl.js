for (i of document.getElementsByClassName("lista2")) {
    console.log(
        i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].getAttribute("onmouseover").match("(http.*?jpg)")[0],
        "https://rarbgprx.org" + i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].getAttribute("href")
    )
}
var a_list = document.getElementById("pager_links").getElementsByTagName("a")
setTimeout("a_list[a_list.length-1].click()",5000)

