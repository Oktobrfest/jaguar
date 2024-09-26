class ImageCrop {
    constructor(url, tags = [], text = '') {
        this.url = url;
        this.tags = tags;
        this.text = text;
    }

    addTag(tag) {
        if (!this.tags.includes(tag)) {
            this.tags.push(tag);
        }
    }

    removeTag(tag) {
        this.tags = this.tags.filter(t => t !== tag);
    }

    setText(text) {
        this.text = text;
    }
    
}



