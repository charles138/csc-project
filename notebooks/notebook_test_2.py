# Databricks notebook source
dbutils.widgets.text("top_k", "5")
top_k = int(dbutils.widgets.get("top_k"))
dbutils.widgets.text("top_l", "6")
top_l = int(dbutils.widgets.get("top_l"))

print(top_k, top_l, top_k * top_l)
