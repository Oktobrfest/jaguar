import React, { useRef, useEffect, useState } from 'react';

import Gallery from './gallery';
import 'react-image-crop/dist/ReactCrop.css'
import Cropper from './Cropper';
import AiAnswer from './AiAnswer';


const CropFest = () => {
    const [ images, setImages ] = useState([]);
    const [ selectedImage, setSelectedImage ] = useState('');
    const [ showCropper, setShowCropper ] = useState(false);
    const [ croppedImages, setCroppedImages ] = useState([]);
    const [ aiResponse, setAiResponse ] = useState('');
    const [ submitCropToApi, setSubmitCropToApi ] = useState(false);

    const UPLOAD_CROPPED_URL = flask_util.url_for('api.upload_cropped');

    // Function to fetch latest images
    const fetchImages = async () => {
        // const response = await fetch('/api/images');
        const response = await fetch(`/api/images?_=${new Date().getTime()}`);

        const data = await response.json();
        if (response.ok) {
            setImages(data.sort((a, b) => b.original.localeCompare(a.original)));
        } else {
            console.error('Failed to fetch images');
        }
    };

    useEffect(() => {
        fetchImages();
        const interval = setInterval(fetchImages, 2.7 * 1000);
        return () => clearInterval(interval);
    }, []);

    const handleSelectImage = (imageUrl) => {
        setSelectedImage(imageUrl);
        // show cropper when a pic is selected
        setShowCropper(true);
    };

    const handleImageCropped = (croppedImageData) => {
        const newCroppedImages = [ ...croppedImages, croppedImageData ];
        setCroppedImages(newCroppedImages);
        setShowCropper(false);
    };

    useEffect(() => {
        if (submitCropToApi && croppedImages.length > 0) {
            sendImagesToAPI();
            setSubmitCropToApi(false);
        }
    }, [croppedImages, submitCropToApi]);


    const sendImagesToAPI = async () => {
        setAiResponse(null);
        try {
            if (!croppedImages) {
                alert('no cropped images present!')
            } else {
                const formData = new FormData();
                let img_no = 1;
                for (let image of croppedImages) {
                    const cropped_img_response = await fetch(image);
                    if (!cropped_img_response.ok) throw new Error('Failed to fetch local image from React');
                    const blob = await cropped_img_response.blob();
                    formData.append('images', blob, `${ img_no }.png`);
                    img_no += 1;
                }

                const uploadResponse = await fetch(UPLOAD_CROPPED_URL, {
                    method: 'POST',
                    body: formData,
                });

                if (uploadResponse.ok) {
                    const result = await uploadResponse.json();
                    setAiResponse(result.ai_response);
                    closeCropper();
                } else {
                    const errorResult = await uploadResponse.json();
                    console.error('Failed to send images', errorResult);
                }
            }
        } catch (error) {
            console.error('Failed to send images', error);
        }
    };
    

    // Remove all crops & close
    function closeCropper(e = null) {
        setShowCropper(false);
        setSelectedImage('');
        setCroppedImages([]);
    }

    // Cancel Current Crop
    function cancelCrop(e) {
        setShowCropper(false);
        setSelectedImage('');
    }


    return (
        <div>
             { !showCropper && (
            <Gallery onSelectImage={ handleSelectImage }
                     items={ images }
                     showBullets={ true }
                // bulletClass="my-custom-bullet"
                // bulletActiveClass="my-custom-bullet-active"
            />
             )}
            { showCropper && (
                <div id="cropper">
                    <Cropper src={ selectedImage }
                             onCropComplete={ handleImageCropped }
                             submitCropToApi={ () => setSubmitCropToApi(true) }
                             closeCropper={ closeCropper }
                             cancelCrop={ cancelCrop }
                    />
                </div>
            ) }
            { croppedImages.length > 0 && (
                <div id="cropped-images-gallery-container">
                    <h2>Cropped Images Gallery</h2>
                    <Gallery items={ croppedImages.map(
                        img => ({ original: img, thumbnail: img })) }/>
                    <button className="button" id="close-cropper-btn" onClick={ closeCropper }>Close Cropper</button>
                    <button className="button" id="send-images-to-api-btn" onClick={ () => setSubmitCropToApi(true) }>Send Images to API
                    </button>
                </div>
            ) }
            { aiResponse && (
                <AiAnswer aiResponse={ aiResponse }/>
            )}

        </div>
    );
};

export { CropFest };