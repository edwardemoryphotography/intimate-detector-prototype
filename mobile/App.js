import React, { useState } from 'react';
import { StyleSheet, Text, View, Button, Image, ActivityIndicator } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

export default function App() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const pickImage = async () => {
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permission.granted) {
      Alert.alert('Permission Required', 'Permission to access the photo library is needed to select an image.');
      return;
    }
    const response = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
    });
    if (!response.canceled) {
      setImage(response.assets[0]);
      setResult(null);
    }
  };

  const uploadImage = async () => {
    if (!image) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', {
      uri: image.uri,
      name: image.fileName || 'photo.jpg',
      type: image.mimeType || 'image/jpeg',
    });
    try {
      const res = await fetch('http://localhost:5000/api/detect', {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Button title="Pick Image" onPress={pickImage} />
      {image && (
        <Image source={{ uri: image.uri }} style={styles.preview} />
      )}
      <Button title="Detect" onPress={uploadImage} disabled={!image || loading} />
      {loading && <ActivityIndicator style={{ marginTop: 10 }} />}
      {result && (
        <View style={styles.resultBox}>
          <Text>Result:</Text>
          <Text>{JSON.stringify(result, null, 2)}</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  preview: {
    width: 200,
    height: 200,
    marginVertical: 10,
  },
  resultBox: {
    marginTop: 20,
    width: '100%',
  },
});
