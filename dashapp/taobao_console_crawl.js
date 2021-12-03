var item_count = sessionStorage.getItem('item_count')
if (item_count == null) {
    item_count = 0
}


var order_lists = document.evaluate("//div[contains(@class,'js-order-container')]", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null)
for (var i = 0; i < order_lists.snapshotLength; i++) {
    var item_date = document.evaluate(".//span[contains(@class,'create-time')]/text()", order_lists.snapshotItem(i), null, XPathResult.STRING_TYPE, null).stringValue
    var item_price = document.evaluate(".//tbody/tr/td[5]//strong/span[2]//text()", order_lists.snapshotItem(i), null, XPathResult.STRING_TYPE, null).stringValue
    var item_status = document.evaluate(".//tbody/tr/td[6]/div/p/span/text()", order_lists.snapshotItem(i), null, XPathResult.STRING_TYPE, null).stringValue
    item = [item_date, item_price, item_status]
    item_count++
    console.log(item_count)
    sessionStorage.setItem(item_count, item)
    sessionStorage.setItem('item_count', item_count)
}

var next_page = document.evaluate("//li[@title='下一页']/a", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
next_page.click()






//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




var item_count = sessionStorage.getItem('item_count')
for (var i = 0; i <= item_count; i++) {
    var item = sessionStorage.getItem(i)
    if (item != null) {
        console.log(item)
    }
}