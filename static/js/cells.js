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
            this.filename = video.substring(14)
        }
        this.title = title
        this.video = video
        this.scale = scale
    }
}

function getVideoId(url){
    let urlparts = url.split('/')
    urlparts = urlparts[urlparts.length - 1].split('=')
    let videoId = urlparts[urlparts.length -1]
    return videoId
}
class YoutubeCell extends Cell {
    constructor(id, title, youtube, scale) {
        super(id)
        this.title = title
        this.youtube = youtube
        this.scale = scale
    }
    embedUrl(){
        let videoId = getVideoId(this.youtube)
        this.youtube =  'https://www.youtube.com/embed/' + videoId
        return this.youtube
    }
}

class AudioCell extends Cell {
    constructor(id, title, audio) {
        super(id)
        if (audio){
            this.editMode = false
            this.filename = audio.substring(14)
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
            this.filename = image.substring(14)
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