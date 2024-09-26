import React, { useState } from 'react';
import ReactCrop from 'react-image-crop';
import 'react-image-crop/dist/ReactCrop.css';
import Gallery from 'react-photo-gallery';
import { Resizable } from 're-resizable';

function ImageEditor() {
    const [src, setSrc] = useState(null);
    const [crop, setCrop] = useState({ aspect: 16 / 9 });
    const [croppedImageUrl, setCroppedImageUrl] = useState(null);
    const [images, setImages] = useState([]);

    const onImageLoaded = image => {
      // handle image load
    };

    const onCropComplete = (crop, pixelCrop) => {
      // handle crop complete
    };

    const onCropChange = crop => {
      setCrop(crop);
    };

    const onSelectFile = e => {
      // handle file select
    };

    return (
        <div>
            <input type="file" accept="image/*" onChange={onSelectFile} />
            {src && (
                <ReactCrop
                    src={src}
                    crop={crop}
                    onImageLoaded={onImageLoaded}
                    onComplete={onCropComplete}
                    onChange={onCropChange}
                />
            )}
            {croppedImageUrl && (
                <img alt="Crop" style={{ maxWidth: '100%' }} src={croppedImageUrl} />
            )}
            <Resizable>
                <Gallery photos={images.map(img => ({ src: img.url, width: 4, height: 3 }))} />
            </Resizable>
        </div>
    );
}

export default ImageEditor;
