var item_count = sessionStorage.getItem('item_count')
if (item_count == null) {
    item_count = 0
}
for (i of document.getElementsByClassName("lista2")) {
    item = [
        i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].text,
        i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].getAttribute("onmouseover").match("(http.*?jpg)")[0],
        "https://rarbgprx.org" + i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].getAttribute("href")
    ]
    item_count++
    console.log(item_count)
    sessionStorage.setItem(item_count, item)
    sessionStorage.setItem('item_count', item_count)
}
var a_list = document.getElementById("pager_links").getElementsByTagName("a")
a_list[a_list.length - 1].click()


var item_count = sessionStorage.getItem('item_count')
for (var i = 0; i <= item_count; i++) {
    var item = sessionStorage.getItem(i)
    if (item != null) {
        console.log(item)
    }
}












// var data = new Array()
// var page_count = 1
// var max = 3
// var intervalId = null


// function crawl() {
//     console.log("当前页码：" + page_count)

//     if (page_count > max) {
//         clearInterval(intervalId)
//         console.log("结束循环...")
//     }

//     for (i of document.getElementsByClassName("lista2")) {
//         item = [
//             i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].text,
//             i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].getAttribute("onmouseover").match("(http.*?jpg)")[0],
//             "https://rarbgprx.org" + i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].getAttribute("href")
//         ]
//         data.push(item)
//     }
//     console.log(data)

//     page_count++

//     var a_list = document.getElementById("pager_links").getElementsByTagName("a")
//     a_list[a_list.length - 1].click()
// }

// intervalId = setInterval(crawl, 5000)










// var page_count = 1
// var max = 3
// var intervalId = null


// function crawl() {
//     console.log("当前页码：" + page_count)

//     if (page_count > max) {
//         clearInterval(intervalId)
//         console.log("结束循环...")
//     }

//     for (i of document.getElementsByClassName("lista2")) {
//         item = [
//             i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].text,
//             i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].getAttribute("onmouseover").match("(http.*?jpg)")[0],
//             "https://rarbgprx.org" + i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].getAttribute("href")
//         ]
//         data.push(item)
//     }
//     console.log(data)

//     page_count++

//     var a_list = document.getElementById("pager_links").getElementsByTagName("a")
//     a_list[a_list.length - 1].click()
// }

// intervalId = setInterval(crawl, 5000)










// var data = new Array()

// for (var page_count = 1; page_count < 3; page_count++) {
//     console.log("当前页码：" + page_count)
//     for (i of document.getElementsByClassName("lista2")) {
//         item = [
//             i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].text,
//             i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].getAttribute("onmouseover").match("(http.*?jpg)")[0],
//             "https://rarbgprx.org" + i.getElementsByClassName("lista")[1].getElementsByTagName("a")[0].getAttribute("href")
//         ]
//         data.push(item)
//     }
//     var a_list = document.getElementById("pager_links").getElementsByTagName("a")
//     setTimeout("a_list[a_list.length-1].click()", 5000)
// }

// console.log(data)