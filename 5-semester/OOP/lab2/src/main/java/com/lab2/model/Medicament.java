package com.lab2.model;

import java.util.ArrayList;
import java.util.List;

public class Medicament {
    private String id;
    private boolean prescription;
    private String name;
    private String pharm;
    private GroupType group;
    private List<String> analogs = new ArrayList<>();
    private List<Version> versions = new ArrayList<>();

    // Getters and Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public boolean isPrescription() { return prescription; }
    public void setPrescription(boolean prescription) { this.prescription = prescription; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getPharm() { return pharm; }
    public void setPharm(String pharm) { this.pharm = pharm; }

    public GroupType getGroup() { return group; }
    public void setGroup(GroupType group) { this.group = group; }

    public List<String> getAnalogs() { return analogs; }
    public void setAnalogs(List<String> analogs) { this.analogs = analogs; }

    public List<Version> getVersions() { return versions; }
    public void setVersions(List<Version> versions) { this.versions = versions; }

    @Override
    public String toString() {
        return "Medicament{id='" + id + "', name='" + name + "', pharm='" + pharm + "'}";
    }
}