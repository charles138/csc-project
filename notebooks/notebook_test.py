# Databricks notebook source
dbutils.widgets.text("top_k", "5")
top_k = int(dbutils.widgets.get("top_k"))

print(top_k, top_k * top_k)
