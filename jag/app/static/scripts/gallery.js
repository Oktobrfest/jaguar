import ImageGallery from 'react-image-gallery';
import "react-image-gallery/styles/css/image-gallery.css";
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

class Gallery extends React.Component {
  render() {
    const { items, onSelectImage } = this.props;
    return (
      <ImageGallery
        items={items}
        onClick={(event) => onSelectImage && onSelectImage(event.target.src)}
      />
    );
  }
}

Gallery.propTypes = {
  onSelectImage: PropTypes.func,
};

export default Gallery;