package com.exam.task1;

public class ObjectItem {
    String name;
    int code;

    public ObjectItem(String name, int code) {
        this.name = name;
        this.code = code;
    }

    @Override
    public String toString() {
        return name + " (шифр: " + code + ")";
    }
}
