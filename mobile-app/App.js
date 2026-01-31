import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  Image,
  StyleSheet,
  ActivityIndicator,
  ScrollView,
  StatusBar,
  Alert,
  Platform
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';

// Cloud Run API URL - Updated with deployed endpoint
const API_URL = 'https://nailhealth-api-ig7c2nupna-uc.a.run.app/predict';

export default function App() {
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [hasPermission, setHasPermission] = useState(false);

  useEffect(() => {
    (async () => {
      const { status } = await ImagePicker.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const takePhoto = async () => {
    if (!hasPermission) {
      Alert.alert(
        'Permission Required',
        'Camera permission is required to take photos.'
      );
      return;
    }

    try {
      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [1, 1],
        quality: 0.8,
      });

      if (!result.canceled) {
        setImage(result.assets[0].uri);
        setResult(null);
        analyzeNail(result.assets[0].uri);
      }
    } catch (error) {
      console.error('Error taking photo:', error);
      Alert.alert('Error', 'Failed to take photo. Please try again.');
    }
  };

  const pickImage = async () => {
    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [1, 1],
        quality: 0.8,
      });

      if (!result.canceled) {
        setImage(result.assets[0].uri);
        setResult(null);
        analyzeNail(result.assets[0].uri);
      }
    } catch (error) {
      console.error('Error picking image:', error);
      Alert.alert('Error', 'Failed to pick image. Please try again.');
    }
  };

  const analyzeNail = async (imageUri) => {
    setLoading(true);
    setResult(null);

    try {
      // Convert image to base64
      const response = await fetch(imageUri);
      const blob = await response.blob();

      const reader = new FileReader();
      reader.onloadend = async () => {
        try {
          const base64data = reader.result.split(',')[1];

          // Send to API
          const apiResponse = await axios.post(
            API_URL,
            { image: base64data },
            {
              headers: {
                'Content-Type': 'application/json',
              },
              timeout: 120000, // 120 second timeout (first request downloads model)
            }
          );

          setResult(apiResponse.data);
        } catch (error) {
          console.error('API Error:', error);
          Alert.alert(
            'Analysis Failed',
            'Unable to analyze the image. Please check your internet connection and try again.'
          );
        } finally {
          setLoading(false);
        }
      };

      reader.onerror = () => {
        setLoading(false);
        Alert.alert('Error', 'Failed to process image.');
      };

      reader.readAsDataURL(blob);
    } catch (error) {
      console.error('Error analyzing nail:', error);
      setLoading(false);
      Alert.alert('Error', 'Failed to analyze image. Please try again.');
    }
  };

  const resetApp = () => {
    setImage(null);
    setResult(null);
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#FCFCF9" />

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>🏥 NailHealth AI</Text>
          <Text style={styles.subtitle}>
            Detect diseases from nail photos
          </Text>
        </View>

        {/* Action Buttons */}
        {!image && (
          <View style={styles.buttonContainer}>
            <TouchableOpacity
              style={styles.primaryButton}
              onPress={takePhoto}
              activeOpacity={0.8}
            >
              <Text style={styles.primaryButtonText}>📸 Take Photo</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.secondaryButton}
              onPress={pickImage}
              activeOpacity={0.8}
            >
              <Text style={styles.secondaryButtonText}>🖼️ Choose from Gallery</Text>
            </TouchableOpacity>
          </View>
        )}

        {/* Image Preview */}
        {image && (
          <View style={styles.imageContainer}>
            <Image source={{ uri: image }} style={styles.image} />
            {!loading && !result && (
              <TouchableOpacity
                style={styles.retakeButton}
                onPress={resetApp}
              >
                <Text style={styles.retakeButtonText}>🔄 Retake Photo</Text>
              </TouchableOpacity>
            )}
          </View>
        )}

        {/* Loading State */}
        {loading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#32B8C6" />
            <Text style={styles.loadingText}>Analyzing nail image...</Text>
            <Text style={styles.loadingSubtext}>
              Using AI to detect potential health conditions
            </Text>
          </View>
        )}

        {/* Results */}
        {result && !loading && (
          <View style={styles.resultsContainer}>
            <Text style={styles.resultsTitle}>🔍 Analysis Results</Text>

            {/* Nail Sign Detection */}
            <View style={styles.card}>
              <View style={styles.cardHeader}>
                <Text style={styles.cardLabel}>Detected Nail Sign</Text>
              </View>
              <Text style={styles.nailSign}>{result.nail_sign}</Text>
              <View style={styles.confidenceBar}>
                <View
                  style={[
                    styles.confidenceFill,
                    { width: `${result.confidence * 100}%` }
                  ]}
                />
              </View>
              <Text style={styles.confidenceText}>
                Confidence: {(result.confidence * 100).toFixed(1)}%
              </Text>
            </View>

            {/* Clinical Explanation */}
            <View style={styles.card}>
              <View style={styles.cardHeader}>
                <Text style={styles.cardLabel}>⚕️ Clinical Explanation</Text>
              </View>
              <Text style={styles.explanationText}>{result.explanation}</Text>
            </View>

            {/* Disease Predictions */}
            <View style={styles.card}>
              <View style={styles.cardHeader}>
                <Text style={styles.cardLabel}>⚠️ Possible Diseases</Text>
              </View>
              {result.diseases && result.diseases.map((disease, index) => (
                <View key={index} style={styles.diseaseItem}>
                  <View style={styles.diseaseHeader}>
                    <Text style={styles.diseaseRank}>{index + 1}</Text>
                    <View style={styles.diseaseInfo}>
                      <Text style={styles.diseaseName}>{disease.name}</Text>
                      <Text style={styles.diseaseConfidence}>
                        {(disease.confidence * 100).toFixed(0)}% likelihood
                      </Text>
                    </View>
                  </View>
                  <View style={styles.diseaseBar}>
                    <View
                      style={[
                        styles.diseaseBarFill,
                        { width: `${disease.confidence * 100}%` }
                      ]}
                    />
                  </View>
                </View>
              ))}
            </View>

            {/* Recommendations */}
            {result.recommendations && result.recommendations.length > 0 && (
              <View style={styles.card}>
                <View style={styles.cardHeader}>
                  <Text style={styles.cardLabel}>📋 Recommended Actions</Text>
                </View>
                {result.recommendations.map((rec, index) => (
                  <View key={index} style={styles.recommendationItem}>
                    <Text style={styles.bullet}>•</Text>
                    <Text style={styles.recommendationText}>{rec}</Text>
                  </View>
                ))}
              </View>
            )}

            {/* Medical Disclaimer */}
            <View style={styles.disclaimerCard}>
              <Text style={styles.disclaimerTitle}>⚠️ Important Notice</Text>
              <Text style={styles.disclaimerText}>
                This app is for educational purposes only. It is NOT a substitute
                for professional medical advice, diagnosis, or treatment. Always
                consult a qualified healthcare provider for proper medical evaluation.
              </Text>
            </View>

            {/* Action Buttons */}
            <TouchableOpacity
              style={styles.newAnalysisButton}
              onPress={resetApp}
            >
              <Text style={styles.newAnalysisButtonText}>
                🔄 Analyze Another Photo
              </Text>
            </TouchableOpacity>
          </View>
        )}

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>
            Powered by Google Health AI (HAI-DEF)
          </Text>
          <Text style={styles.footerSubtext}>
            MedSigLIP + MedGemma 4B
          </Text>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FCFCF9',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingTop: Platform.OS === 'ios' ? 60 : 40,
  },
  header: {
    alignItems: 'center',
    marginBottom: 30,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#13343B',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#626C71',
    textAlign: 'center',
  },
  buttonContainer: {
    marginBottom: 30,
  },
  primaryButton: {
    backgroundColor: '#32B8C6',
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderRadius: 12,
    marginBottom: 12,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  primaryButtonText: {
    color: '#FFFFFD',
    fontSize: 18,
    fontWeight: '600',
  },
  secondaryButton: {
    backgroundColor: 'rgba(94, 82, 64, 0.12)',
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(94, 82, 64, 0.2)',
  },
  secondaryButtonText: {
    color: '#13343B',
    fontSize: 18,
    fontWeight: '600',
  },
  imageContainer: {
    marginBottom: 20,
  },
  image: {
    width: '100%',
    height: 300,
    borderRadius: 12,
    marginBottom: 12,
  },
  retakeButton: {
    backgroundColor: 'rgba(94, 82, 64, 0.12)',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 8,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(94, 82, 64, 0.2)',
  },
  retakeButtonText: {
    color: '#13343B',
    fontSize: 16,
    fontWeight: '600',
  },
  loadingContainer: {
    alignItems: 'center',
    marginVertical: 40,
  },
  loadingText: {
    marginTop: 16,
    fontSize: 18,
    fontWeight: '600',
    color: '#13343B',
  },
  loadingSubtext: {
    marginTop: 8,
    fontSize: 14,
    color: '#626C71',
    textAlign: 'center',
  },
  resultsContainer: {
    marginTop: 20,
  },
  resultsTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#13343B',
    marginBottom: 20,
  },
  card: {
    backgroundColor: '#FFFFFD',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: 'rgba(94, 82, 64, 0.12)',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 2,
  },
  cardHeader: {
    marginBottom: 12,
  },
  cardLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#626C71',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  nailSign: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#32B8C6',
    marginBottom: 12,
  },
  confidenceBar: {
    height: 8,
    backgroundColor: 'rgba(50, 184, 198, 0.2)',
    borderRadius: 4,
    overflow: 'hidden',
    marginBottom: 8,
  },
  confidenceFill: {
    height: '100%',
    backgroundColor: '#32B8C6',
  },
  confidenceText: {
    fontSize: 14,
    color: '#626C71',
  },
  explanationText: {
    fontSize: 15,
    lineHeight: 22,
    color: '#13343B',
  },
  diseaseItem: {
    marginBottom: 16,
  },
  diseaseHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  diseaseRank: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: '#32B8C6',
    color: '#FFFFFD',
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
    lineHeight: 28,
    marginRight: 12,
  },
  diseaseInfo: {
    flex: 1,
  },
  diseaseName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#13343B',
    marginBottom: 4,
  },
  diseaseConfidence: {
    fontSize: 14,
    color: '#626C71',
  },
  diseaseBar: {
    height: 6,
    backgroundColor: 'rgba(50, 184, 198, 0.2)',
    borderRadius: 3,
    overflow: 'hidden',
    marginLeft: 40,
  },
  diseaseBarFill: {
    height: '100%',
    backgroundColor: '#32B8C6',
  },
  recommendationItem: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  bullet: {
    fontSize: 16,
    color: '#32B8C6',
    marginRight: 8,
    fontWeight: 'bold',
  },
  recommendationText: {
    flex: 1,
    fontSize: 15,
    lineHeight: 22,
    color: '#13343B',
  },
  disclaimerCard: {
    backgroundColor: 'rgba(192, 21, 47, 0.1)',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: 'rgba(192, 21, 47, 0.2)',
  },
  disclaimerTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#C0152F',
    marginBottom: 8,
  },
  disclaimerText: {
    fontSize: 14,
    lineHeight: 20,
    color: '#13343B',
  },
  newAnalysisButton: {
    backgroundColor: '#32B8C6',
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 20,
  },
  newAnalysisButtonText: {
    color: '#FFFFFD',
    fontSize: 18,
    fontWeight: '600',
  },
  footer: {
    alignItems: 'center',
    marginTop: 20,
    marginBottom: 40,
  },
  footerText: {
    fontSize: 12,
    color: '#626C71',
    marginBottom: 4,
  },
  footerSubtext: {
    fontSize: 11,
    color: '#A7A9A9',
  },
});
