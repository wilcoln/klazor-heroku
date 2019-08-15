class Cell {
    constructor(id) {
        this.id = id
        this.editMode = true
        this.selected = true
    }
}

class VideoCell extends Cell {
    constructor(id, title, video, scale) {
        super(id)
        if (video) {
            this.editMode = false
        }
        this.title = title
        this.video = video
        this.scale = scale
    }
}

function getYoutubeVideoId(url){
    url = url.replace('&t', '')
    let urlparts = url.split('/')
    urlparts = urlparts[urlparts.length - 1].split('=')
    let videoId = urlparts.length > 1 ? urlparts[1]: urlparts[0]
    return videoId
}
class YoutubeCell extends Cell {
    constructor(id, title, youtube, scale) {
        super(id)
        this.title = title
        if(youtube)
            this.editMode = false
        this.youtube = youtube
        this.scale = scale
    }
    embedUrl(){
        let videoId = getYoutubeVideoId(this.youtube)
        this.youtube =  'https://www.youtube.com/embed/' + videoId
        return this.youtube
    }
}
class AudioCell extends Cell {
    constructor(id, title, audio) {
        super(id)
        if (audio){
            this.editMode = false
        }
        this.title = title
        this.audio = audio
    }
}

class ImageCell extends Cell {
    constructor(id, title, image, scale) {
        super(id)
        if (image){
            this.editMode = false
        }
        this.title = title
        this.image = image
        this.scale = scale
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

class FileCell extends Cell {
    constructor(id, title, url) {
        super(id)
        if (url){
            this.editMode = false
        }
        this.title = title
        this.url = url
    }
}
class MultipleChoiceQuestionCell extends Cell{
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
class NumericalQuestionCell extends Cell{
    constructor(id, answer){
        super(id)
        this.answer = answer
    }
}
class OpenEndedQuestionCell extends Cell{
    constructor(id, answer){
        super(id)
        this.answer = answer
    }
}
function getFilenameFromUrl(url){
    let urlparts = url.split('/')
    return urlparts[urlparts.length - 1]
}