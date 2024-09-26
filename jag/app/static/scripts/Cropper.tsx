import 'react-image-crop/dist/ReactCrop.css';
import React, { useRef, useState, useEffect } from 'react';
import ReactCrop, {
    centerCrop,
    makeAspectCrop,
    Crop,
    PixelCrop,
    convertToPixelCrop,
} from 'react-image-crop'
import { PercentCrop } from "react-image-crop/src/types";
import { canvasPreview } from "./canvasPreview";
import { useDebounceEffect } from "./useDebounceEffect";

function Cropper({ src, onCropComplete, submitCropToApi, closeCropper, cancelCrop }) {
    const [ completedCrop, setCompletedCrop ] = useState<PercentCrop>()
    const [ imgSrc, setImgSrc ] = useState('')

    const imgRef = useRef<HTMLImageElement>(null)
    const previewCanvasRef = useRef<HTMLCanvasElement>(null);

    const hiddenAnchorRef = useRef<HTMLAnchorElement>(null)
    const blobUrlRef = useRef('')

    const [ aspect, setAspect ] = useState<number | undefined>(undefined);

    const [ crop, setCrop ] = useState<Crop>({
        unit: '%', // Can be 'px' or '%' percent is better!!
        x: 25,
        y: 25,
        width: 50,
        height: 50
    })

    function centerAspectCrop(
        mediaWidth: number,
        mediaHeight: number,
        aspect: number,
    ) {
        return centerCrop(
            makeAspectCrop(
                {
                    unit: '%',
                    width: 90,
                },
                aspect,
                mediaWidth,
                mediaHeight,
            ),
            mediaWidth,
            mediaHeight,
        )
    }

    function onSelectFile(e: React.ChangeEvent<HTMLInputElement>) {
        if (e.target.files && e.target.files.length > 0) {
            setCrop(undefined) // Makes crop preview update between images.
            const reader = new FileReader()
            reader.addEventListener('load', () =>
                setImgSrc(reader.result?.toString() || ''),
            )
            reader.readAsDataURL(e.target.files[0])
        }
    }

    function onImageLoad(e: React.SyntheticEvent<HTMLImageElement>) {
        if (aspect) {
            const { width, height } = e.currentTarget
            setCrop(centerAspectCrop(width, height, aspect))
        }
    }

        // Ensure to update imgSrc when src prop changes
    useEffect(() => {
        setImgSrc(src);
        setCrop({ unit: '%', x: 25, y: 25, width: 50, height: 50 }); // Reset crop
    }, [src]);

    // function closeCropper(e) {
    //     setImgSrc('');        // Clears the image source, effectively removing the image from the UI
    //     setCrop(null);   // Resets the crop area
    //     setCompletedCrop(null);
    //     console.log("Current imgSrc state:", imgSrc);
    //     src = '';
    // }

    // console.log("Current imgSrc state:", imgSrc);
    async function getCroppedImage() {
        const image = imgRef.current
        const previewCanvas = previewCanvasRef.current
        if (!image || !previewCanvas || !completedCrop) {
            throw new Error('Crop canvas does not exist')
        }

        // This will size relative to the uploaded image
        // size. If you want to size according to what they
        // are looking at on screen, remove scaleX + scaleY
        const scaleX = image.naturalWidth / image.width
        const scaleY = image.naturalHeight / image.height

        const offscreen = new OffscreenCanvas(
            completedCrop.width * scaleX,
            completedCrop.height * scaleY,
        )
        const ctx = offscreen.getContext('2d')
        if (!ctx) {
            throw new Error('No 2d context')
        }

        ctx.drawImage(
            previewCanvas,
            0,
            0,
            previewCanvas.width,
            previewCanvas.height,
            0,
            0,
            offscreen.width,
            offscreen.height,
        )
        // You might want { type: "image/jpeg", quality: <0 to 1> } to
        // reduce image size
        const blob = await offscreen.convertToBlob({
            type: 'image/png',
        })

        const newCroppedImage = URL.createObjectURL(blob);
        onCropComplete(newCroppedImage);

        // to download crop directly to local machine (original code)
        // if (blobUrlRef.current) {
        //     URL.revokeObjectURL(blobUrlRef.current)
        // }
        // blobUrlRef.current = URL.createObjectURL(blob)
        //
        // if (hiddenAnchorRef.current) {
        //     hiddenAnchorRef.current.href = blobUrlRef.current
        //     hiddenAnchorRef.current.click()
        // }
    }

    useDebounceEffect(
        async () => {
            if (
                completedCrop?.width &&
                completedCrop?.height &&
                imgRef.current &&
                previewCanvasRef.current
            ) {
                // We use canvasPreview as it's much faster than imgPreview.
                canvasPreview(
                    imgRef.current,
                    previewCanvasRef.current,
                    completedCrop
                )
            }
        },
        100,
        [ completedCrop ],
    )

    const onCropChange = (crop, percentCrop) => setCrop(percentCrop)

    const cropNsendToApi = async () => {
        await getCroppedImage();
        submitCropToApi();
    }


    return (
        <div className="App">
            { !!src ?
                (
                    <ReactCrop
                        crop={ crop }
                        onChange={ onCropChange }
                        onComplete={ (c) => setCompletedCrop(c) }
                        aspect={ aspect }
                        minHeight={ 100 }
                    >
                        <img
                            ref={ imgRef }
                            alt="Crop me"
                            src={ src }
                            onLoad={ onImageLoad }
                        />
                    </ReactCrop>
                ) : <img
                    alt="Crop me"
                    src={ src }
                    onLoad={ onImageLoad }
                />
            }
            { !!completedCrop && (
                <>
                    <div>
                        <canvas
                            ref={ previewCanvasRef }
                            style={ {
                                border: '1px solid black',
                                objectFit: 'contain',
                                width: completedCrop.width,
                                height: completedCrop.height,
                                display: 'none',
                            } }
                        />
                    </div>
                    <div>
                        <button className="button" id="cancel-crop-btn" onClick={ cancelCrop }>Cancel</button>
                        <button className="button" id="crop-img-btn" onClick={ getCroppedImage }>Crop Image</button>
                        <button className="button" id="crop-n-send-btn" onClick={ cropNsendToApi }>Crop & Send</button>
                    </div>
                </>
            ) }
        </div>
    )
}

export default Cropper;
