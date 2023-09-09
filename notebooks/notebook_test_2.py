# Databricks notebook source
dbutils.widgets.text("top_m", "5")
top_m = int(dbutils.widgets.get("top_m"))
dbutils.widgets.text("top_n", "6")
top_n = int(dbutils.widgets.get("top_n"))

print(top_m, top_n, top_m * top_n)
