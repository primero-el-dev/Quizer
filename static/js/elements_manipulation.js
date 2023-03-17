const swapTheSameElements = (first, second, replacePattern) => {
    let items = $(first).parent().children()
    let firstIndex, secondIndex;
    for (let i = 0; i < items.length; i++) {
        if (items[i] == first) {
            firstIndex = i
        }
        if (items[i] == second) {
            secondIndex = i
        }
    }

    let min = Math.min(firstIndex, secondIndex)
    let max = Math.max(firstIndex, secondIndex)
    if (max - min > 1) {
        $(items[max]).insertAfter($(items[min]))
        $(items[min]).insertAfter($(items[max-1]))
    } else {
        $(items[max]).insertAfter($(items[min]))
        $(items[min]).insertAfter($(items[max]))
    }

    updateChildrenNameIndexes($(items[0]).parent(), replacePattern)
}

const replaceHtmlAttributeValue = (element, attribute, replacePattern, replacement) => {
    $(element).find(`[${attribute}]`).each(
        (_, item) => $(item).attr(attribute, $(item).attr(attribute).replace(replacePattern, replacement))
    )
}

const updateChildrenNameIndexes = (element, replacePattern) => {
    let items = $(element).children()
    for (let i = 0; i < items.length; i++) {
        replaceHtmlAttributeValue(items[i], 'name', replacePattern, i)
    }
}

const moveDown = (selector, pattern) => e => {
    let element = $(e.target).closest(selector)
    let next = element.next()
    if (next[0] != undefined) {
        swapTheSameElements(element[0], next[0], pattern)
    }
}

const moveUp = (selector, pattern) => e => {
    let element = $(e.target).closest(selector)
    let prev = element.prev()
    if (prev[0] != undefined) {
        swapTheSameElements(element[0], prev[0], pattern)
    }
}

const deleteClosest = (selector, pattern) => e => {
    let parent = $(e.target).closest(selector).parent()
    $(e.target).closest(selector).remove()

    updateChildrenNameIndexes(parent, pattern)
}