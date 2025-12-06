package com.lab2;

import org.junit.jupiter.api.Test;

import com.lab2.tool.ValidatorXSD;

import java.io.File;
import static org.junit.jupiter.api.Assertions.*;

class ValidatorXSDTest {

    @Test
    void testIsValidWithCorrectFile() {
        File xmlFile = new File("src/main/resources/Medicine.xml");
        File xsdFile = new File("src/main/resources/Medicine.xsd");

        assertTrue(xmlFile.exists(), "XML file needs to exist for test");
        assertTrue(xsdFile.exists(), "XSD file needs to exist for test");

        boolean isValid = ValidatorXSD.isValid(xmlFile, xsdFile);
        assertTrue(isValid, "Validation should pass for valid XML");
    }

    @Test
    void testInvalidFileDates() {
        File xmlFile = new File("fake.xml");
        File xsdFile = new File("fake.xsd");

        boolean isValid = ValidatorXSD.isValid(xmlFile, xsdFile);
        assertFalse(isValid, "Validation should fail for missing files");
    }

    @Test
    void testValidatorWithNullArgs() {
        boolean result = ValidatorXSD.isValid(null, null);
        assertFalse(result, "Should return false for null files");
    }

    @Test
    void testValidatorWithDirectoryInsteadOfFile() {
        File dir = new File("src/main/resources");
        boolean result = ValidatorXSD.isValid(dir, dir);
        assertFalse(result, "Should fail if path is a directory");
    }
}