class Cell {
    constructor(id) {
        this.id = id
        this.editMode = true
        this.selected = true
    }
}
class MediaCell extends Cell{
    constructor(id, title, url) {
        super(id)
        if (url) {
            this.editMode = false
        }
        this.title = title
        this.url = url
    }
}
class GraphicMediaCell extends  MediaCell{
    constructor(id, title, url, scale){
        super(id, title, url)
        this.scale = scale
    }
}
class VideoCell extends GraphicMediaCell {
    constructor(id, title, url, scale){
        super(id, title, url, scale)
    }
}

function getYoutubeVideoId(url){
    url = url.replace('&t', '')
    let urlparts = url.split('/')
    urlparts = urlparts[urlparts.length - 1].split('=')
    let videoId = urlparts.length > 1 ? urlparts[1]: urlparts[0]
    return videoId
}
class YoutubeCell extends GraphicMediaCell {
    constructor(id, title, url, scale) {
        super(id, title, url, scale)
    }
    embedUrl(){
        let videoId = getYoutubeVideoId(this.url)
        this.url =  'https://www.youtube.com/embed/' + videoId
        return this.url
    }
}
class AudioCell extends MediaCell {
    constructor(id, title, url) {
        super(id, title, url)
    }
}

class ImageCell extends Cell {
   constructor(id, title, url, scale){
        super(id, title, url, scale)
    }
}

class MarkdownCell extends Cell {
    constructor(id, text) {
        super(id)
        if (text)
            this.editMode = false
        this.text = text
    }
}

class FileCell extends MediaCell {
    constructor(id, title, url){
        super(id, title, url)
    }
}
class MultipleChoiceInputCell extends Cell{
    constructor(id){
        super(id)
        this.propositions = []
        this.nbPropositions = 0

    }
    addProposition(statement, truthValue){
        this.propositions.push(new Proposition(statement, truthValue))
    }
    getNbChecked(){
        let result = 0
        for(let proposition of this.propositions)
            if(proposition.isTrue)
                result++
        console.log(result)
        return result
    }
}
class Proposition{
    constructor(statement, truthValue){
        this.statement = statement
        this.isTrue = truthValue
    }
}
class NumericalInputCell extends Cell{
    constructor(id, answer){
        super(id)
        this.answer = answer
    }
}
class OpenEndedInputCell extends Cell{
    constructor(id, answer){
        super(id)
        this.answer = answer
    }
}
function getFilenameFromUrl(url){
    let urlparts = url.split('/')
    return urlparts[urlparts.length - 1]
}