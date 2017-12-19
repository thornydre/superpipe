#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from tkinter import *
from Resources import *
from Shot import *
from os import path
from io import StringIO

import json

class StatisticsView(Frame):
    def __init__(self, parent):
        ## THEME COLORS ##
        self.theme = Resources.readLine("save/options.spi", 2)
        self.main_color = Resources.readLine("save/themes/" + self.theme + ".spi", 1)
        self.second_color = Resources.readLine("save/themes/" + self.theme + ".spi", 2)
        self.list_color = Resources.readLine("save/themes/" + self.theme + ".spi", 3)
        self.button_color1 = Resources.readLine("save/themes/" + self.theme + ".spi", 4)
        self.over_button_color1 = Resources.readLine("save/themes/" + self.theme + ".spi", 5)
        self.button_color2 = Resources.readLine("save/themes/" + self.theme + ".spi", 6)
        self.over_button_color2 = Resources.readLine("save/themes/" + self.theme + ".spi", 7)
        self.separator_color = Resources.readLine("save/themes/" + self.theme + ".spi", 8)
        self.text_color = Resources.readLine("save/themes/" + self.theme + ".spi", 9)
        self.done_color = Resources.readLine("save/themes/" + self.theme + ".spi", 12)
        self.urgent_color = Resources.readLine("save/themes/" + self.theme + ".spi", 13)
        self.high_color = Resources.readLine("save/themes/" + self.theme + ".spi", 14)
        self.medium_color = Resources.readLine("save/themes/" + self.theme + ".spi", 15)
        self.done_select_color = Resources.readLine("save/themes/" + self.theme + ".spi", 16)
        self.urgent_select_color = Resources.readLine("save/themes/" + self.theme + ".spi", 17)
        self.high_select_color = Resources.readLine("save/themes/" + self.theme + ".spi", 18)
        self.medium_select_color = Resources.readLine("save/themes/" + self.theme + ".spi", 19)
        self.stat_list_color1 = Resources.readLine("save/themes/" + self.theme + ".spi", 20)
        self.stat_list_color2 = Resources.readLine("save/themes/" + self.theme + ".spi", 21)

        super().__init__(parent, bg = self.main_color, bd = 0)

    def set(self, project):
        self.project = project

        if self.project.getShotList():
            self.project_stats_path = self.project.getDirectory() + "/project_stats.spi"

            if not path.isfile(self.project_stats_path):
                open(self.project_stats_path, "a").close()

            with open(self.project_stats_path, "r") as f:
                str_stats = f.read()
            f.close()

            stats_label = Label(self, text = "STATISTICS", bg = self.main_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 11 bold")
            stats_label.pack(expand = True, fill = BOTH, pady = 10)

            general_stats_area = Frame(self, bg = self.second_color, bd = 0)
            general_stats_area.pack(expand = True, fill = BOTH)

            ## HEADER ##
            separator1_area = Frame(self, bg = self.separator_color, height = 2, bd = 0)
            separator1_area.pack(expand = True, fill = BOTH)

            self.stats_shots_header_area = Frame(self, bg = self.main_color, bd = 0)
            self.stats_shots_header_area.pack(expand = True, fill = BOTH)

            self.stats_shots_header_area.columnconfigure(0, weight = 1)
            self.stats_shots_header_area.columnconfigure(1, weight = 1)
            self.stats_shots_header_area.columnconfigure(2, weight = 1)
            self.stats_shots_header_area.columnconfigure(3, weight = 1)
            self.stats_shots_header_area.columnconfigure(4, weight = 1)
            self.stats_shots_header_area.columnconfigure(5, weight = 1)

            shot_header_label = Label(self.stats_shots_header_area, text = "shot", bg = self.main_color, fg = self.text_color)
            shot_header_label.grid(row = 0, column = 0, pady = 5, padx = 10)

            shot_frame_range_header_label = Label(self.stats_shots_header_area, text = "frame range", bg = self.main_color, fg = self.text_color)
            shot_frame_range_header_label.grid(row = 0, column = 1, pady = 5, padx = 10)

            shot_frame_range_header_label = Label(self.stats_shots_header_area, text = "animation", bg = self.main_color, fg = self.text_color)
            shot_frame_range_header_label.grid(row = 0, column = 2, pady = 5, padx = 10)

            shot_frame_range_header_label = Label(self.stats_shots_header_area, text = "lighting", bg = self.main_color, fg = self.text_color)
            shot_frame_range_header_label.grid(row = 0, column = 3, pady = 5, padx = 10)

            shot_frame_range_header_label = Label(self.stats_shots_header_area, text = "rendering", bg = self.main_color, fg = self.text_color)
            shot_frame_range_header_label.grid(row = 0, column = 4, pady = 5, padx = 10)

            shot_frame_range_header_label = Label(self.stats_shots_header_area, text = "compositing", bg = self.main_color, fg = self.text_color)
            shot_frame_range_header_label.grid(row = 0, column = 5, pady = 5, padx = 10)

            separator2_area = Frame(self, bg = self.separator_color, height = 2, bd = 0)
            separator2_area.pack(expand = True, fill = BOTH)

            stats_shots_area = Frame(self, bg = self.main_color, bd = 0)
            stats_shots_area.pack(expand = True, fill = BOTH)

            ## SHOTS STATS ##
            i = 0
            done_shots = 0
            animations_states = {"To do" : 0, "WIP" : 0, "Done" : 0}
            lightings_states = {"To do" : 0, "WIP" : 0, "Done" : 0}
            renderings_states = {"To do" : 0, "WIP" : 0, "Done" : 0}
            compositings_states = {"To do" : 0, "WIP" : 0, "Done" : 0}

            self.shot_label_list = []
            self.shot_text_list = []
            self.shot_frame_range_label_list = []
            self.shot_frame_range_text_list = []

            self.animation_menu_list = {}
            self.lighting_menu_list = {}
            self.rendering_menu_list = {}
            self.compositing_menu_list = {}

            self.vars_shot_animation = {}
            self.vars_shot_lighting = {}
            self.vars_shot_rendering = {}
            self.vars_shot_compositing = {}

            self.stats_dict = {}

            for shot in self.project.getShotList():
                cur_shot = Shot(self.project.getDirectory(), shot[1])

                if i % 2 == 0:
                    shot_line = Frame(self, bg = self.stat_list_color1, bd = 0)
                    shot_line.pack(expand = True, fill = BOTH)
                else:
                    shot_line = Frame(self, bg = self.stat_list_color2, bd = 0)
                    shot_line.pack(expand = True, fill = BOTH)

                shot_line.columnconfigure(0, weight = 1)
                shot_line.columnconfigure(1, weight = 1)
                shot_line.columnconfigure(2, weight = 1)
                shot_line.columnconfigure(3, weight = 1)
                shot_line.columnconfigure(4, weight = 1)
                shot_line.columnconfigure(5, weight = 1)

                shot_text = StringVar()
                self.shot_text_list.append(shot_text)
                self.shot_text_list[i].set(shot[1])
                shot_label = Label(shot_line, textvariable = self.shot_text_list[i], bg = shot_line.cget("bg"), fg = self.text_color)
                shot_label.grid(row = shot[0], column = 0, pady = 5, padx = 10)
                self.shot_label_list.append(shot_label)

                shot_frame_range_text = StringVar()
                self.shot_frame_range_text_list.append(shot_frame_range_text)
                self.shot_frame_range_text_list[i].set(cur_shot.getFrameRange())
                shot_frame_range_label = Label(shot_line, textvariable = self.shot_frame_range_text_list[i], bg = shot_line.cget("bg"), fg = self.text_color)
                shot_frame_range_label.grid(row = shot[0], column = 1, pady = 5, padx = 10)
                self.shot_frame_range_label_list.append(shot_frame_range_label)

                self.vars_shot_animation[shot[1]] = StringVar()
                self.vars_shot_lighting[shot[1]] = StringVar()
                self.vars_shot_rendering[shot[1]] = StringVar()
                self.vars_shot_compositing[shot[1]] = StringVar()
                if str_stats:
                    self.stats_dict = json.loads(str_stats)
                    if self.stats_dict[shot[1]]:
                        self.vars_shot_animation[shot[1]].set(self.stats_dict[shot[1]][0])
                        if self.stats_dict[shot[1]][0]:
                            animations_states[self.stats_dict[shot[1]][0]] += 1

                        self.vars_shot_lighting[shot[1]].set(self.stats_dict[shot[1]][1])
                        if self.stats_dict[shot[1]][1]:
                            lightings_states[self.stats_dict[shot[1]][1]] += 1

                        self.vars_shot_rendering[shot[1]].set(self.stats_dict[shot[1]][2])
                        if self.stats_dict[shot[1]][2]:
                            renderings_states[self.stats_dict[shot[1]][2]] += 1

                        self.vars_shot_compositing[shot[1]].set(self.stats_dict[shot[1]][3])
                        if self.stats_dict[shot[1]][3]:
                            compositings_states[self.stats_dict[shot[1]][3]] += 1
                    else:
                        self.vars_shot_animation[shot[1]].set("To do")
                        self.vars_shot_lighting[shot[1]].set("To do")
                        self.vars_shot_rendering[shot[1]].set("To do")
                        self.vars_shot_compositing[shot[1]].set("To do")

                else:
                    self.vars_shot_animation[shot[1]].set("To do")
                    self.vars_shot_lighting[shot[1]].set("To do")
                    self.vars_shot_rendering[shot[1]].set("To do")
                    self.vars_shot_compositing[shot[1]].set("To do")

                animation_menu = OptionMenu(shot_line, self.vars_shot_animation[shot[1]], "To do", "WIP", "Done", command = self.statisticsMenuCommand)
                animation_menu.config(bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, bd = 0, width = 8, highlightthickness = 0)
                animation_menu.grid(row = shot[0], column = 2, pady = 5, padx = 10)
                self.animation_menu_list[shot[1]] = animation_menu

                lighting_menu = OptionMenu(shot_line, self.vars_shot_lighting[shot[1]], "To do", "WIP", "Done", command = self.statisticsMenuCommand)
                lighting_menu.config(bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, bd = 0, width = 8, highlightthickness = 0)
                lighting_menu.grid(row = shot[0], column = 3, pady = 5, padx = 10)
                self.lighting_menu_list[shot[1]] = lighting_menu

                rendering_menu = OptionMenu(shot_line, self.vars_shot_rendering[shot[1]], "To do", "WIP", "Done", command = self.statisticsMenuCommand)
                rendering_menu.config(bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, bd = 0, width = 8, highlightthickness = 0)
                rendering_menu.grid(row = shot[0], column = 4, pady = 5, padx = 10)
                self.rendering_menu_list[shot[1]] = rendering_menu

                compositing_menu = OptionMenu(shot_line, self.vars_shot_compositing[shot[1]], "To do", "WIP", "Done", command = self.statisticsMenuCommand)
                compositing_menu.config(bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, bd = 0, width = 8, highlightthickness = 0)
                compositing_menu.grid(row = shot[0], column = 5, pady = 5, padx = 10)
                self.compositing_menu_list[shot[1]] = compositing_menu

                if cur_shot.isDone():
                    done_shots += 1

                i += 1

            ## GENERAL STATS ##
            number_of_shots_label = Label(general_stats_area, text = str(len(self.project.getShotList())) + " SHOTS", bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            number_of_shots_label.grid(row = 0, column = 0, pady = 5, padx = 10)

            self.done_shots_text = StringVar()
            self.done_shots_text.set(str(done_shots) + " done shot (" + str(round(done_shots / len(self.project.getShotList()) * 100)) + "%)")
            number_of_done_shots_label = Label(general_stats_area, textvariable = self.done_shots_text, bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            number_of_done_shots_label.grid(row = 1, column = 0, pady = 5, padx = 10)

            general_to_do_label = Label(general_stats_area, text = "TO DO", bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            general_to_do_label.grid(row = 2, column = 1, pady = 5, padx = 10)

            general_wip_label = Label(general_stats_area, text = "WIP", bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            general_wip_label.grid(row = 2, column = 2, pady = 5, padx = 10)

            general_done_label = Label(general_stats_area, text = "DONE", bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            general_done_label.grid(row = 2, column = 3, pady = 5, padx = 10)

            #ANIMATION#
            general_animation_label = Label(general_stats_area, text = "ANIMATION", bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            general_animation_label.grid(row = 3, column = 0, pady = 5, padx = 10)

            self.animation_to_do_text = StringVar()
            self.animation_to_do_text.set(str(round(animations_states["To do"] / len(self.project.getShotList()) * 100)) + "%")
            animation_to_do_label = Label(general_stats_area, textvariable = self.animation_to_do_text, bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            animation_to_do_label.grid(row = 3, column = 1, pady = 5, padx = 10)

            self.animation_wip_text = StringVar()
            self.animation_wip_text.set(str(round(animations_states["WIP"] / len(self.project.getShotList()) * 100)) + "%")
            animation_wip_label = Label(general_stats_area, textvariable = self.animation_wip_text, bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            animation_wip_label.grid(row = 3, column = 2, pady = 5, padx = 10)

            self.animation_done_text = StringVar()
            self.animation_done_text.set(str(round(animations_states["Done"] / len(self.project.getShotList()) * 100)) + "%")
            animation_done_label = Label(general_stats_area, textvariable = self.animation_done_text, bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            animation_done_label.grid(row = 3, column = 3, pady = 5, padx = 10)

            #LIGHTING#
            general_lighting_label = Label(general_stats_area, text = "LIGHTING", bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            general_lighting_label.grid(row = 4, column = 0, pady = 5, padx = 10)

            self.lighting_to_do_text = StringVar()
            self.lighting_to_do_text.set(str(round(lightings_states["To do"] / len(self.project.getShotList()) * 100)) + "%")
            lighting_to_do_label = Label(general_stats_area, textvariable = self.lighting_to_do_text, bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            lighting_to_do_label.grid(row = 4, column = 1, pady = 5, padx = 10)

            self.lighting_wip_text = StringVar()
            self.lighting_wip_text.set(str(round(lightings_states["WIP"] / len(self.project.getShotList()) * 100)) + "%")
            lighting_wip_label = Label(general_stats_area, textvariable = self.lighting_wip_text, bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            lighting_wip_label.grid(row = 4, column = 2, pady = 5, padx = 10)

            self.lighting_done_text = StringVar()
            self.lighting_done_text.set(str(round(lightings_states["Done"] / len(self.project.getShotList()) * 100)) + "%")
            lighting_done_label = Label(general_stats_area, textvariable = self.lighting_done_text, bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            lighting_done_label.grid(row = 4, column = 3, pady = 5, padx = 10)

            #RENDERING#
            general_rendering_label = Label(general_stats_area, text = "RENDERING", bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            general_rendering_label.grid(row = 5, column = 0, pady = 5, padx = 10)

            self.rendering_to_do_text = StringVar()
            self.rendering_to_do_text.set(str(round(renderings_states["To do"] / len(self.project.getShotList()) * 100)) + "%")
            rendering_to_do_label = Label(general_stats_area, textvariable = self.rendering_to_do_text, bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            rendering_to_do_label.grid(row = 5, column = 1, pady = 5, padx = 10)

            self.rendering_wip_text = StringVar()
            self.rendering_wip_text.set(str(round(renderings_states["WIP"] / len(self.project.getShotList()) * 100)) + "%")
            rendering_wip_label = Label(general_stats_area, textvariable = self.rendering_wip_text, bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            rendering_wip_label.grid(row = 5, column = 2, pady = 5, padx = 10)

            self.rendering_done_text = StringVar()
            self.rendering_done_text.set(str(round(renderings_states["Done"] / len(self.project.getShotList()) * 100)) + "%")
            rendering_done_label = Label(general_stats_area, textvariable = self.rendering_done_text, bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            rendering_done_label.grid(row = 5, column = 3, pady = 5, padx = 10)

            #COMPOSITING#
            general_compositing_label = Label(general_stats_area, text = "COMPOSITING", bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            general_compositing_label.grid(row = 6, column = 0, pady = 5, padx = 10)

            self.compositing_to_do_text = StringVar()
            self.compositing_to_do_text.set(str(round(compositings_states["To do"] / len(self.project.getShotList()) * 100)) + "%")
            compositing_to_do_label = Label(general_stats_area, textvariable = self.compositing_to_do_text, bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            compositing_to_do_label.grid(row = 6, column = 1, pady = 5, padx = 10)

            self.compositing_wip_text = StringVar()
            self.compositing_wip_text.set(str(round(compositings_states["WIP"] / len(self.project.getShotList()) * 100)) + "%")
            compositing_wip_label = Label(general_stats_area, textvariable = self.compositing_wip_text, bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            compositing_wip_label.grid(row = 6, column = 2, pady = 5, padx = 10)

            self.compositing_done_text = StringVar()
            self.compositing_done_text.set(str(round(compositings_states["Done"] / len(self.project.getShotList()) * 100)) + "%")
            compositing_done_label = Label(general_stats_area, textvariable = self.compositing_done_text, bg = self.second_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 9 bold")
            compositing_done_label.grid(row = 6, column = 3, pady = 5, padx = 10)

    def update(self):
        i = 0
        done_shots = 0
        animations_states = {"To do" : 0, "WIP" : 0, "Done" : 0}
        lightings_states = {"To do" : 0, "WIP" : 0, "Done" : 0}
        renderings_states = {"To do" : 0, "WIP" : 0, "Done" : 0}
        compositings_states = {"To do" : 0, "WIP" : 0, "Done" : 0}

        for missing_shot in range(len(self.project.getShotList()) - len(self.shot_text_list)):
            self.shot_text_list.append(StringVar())
            self.shot_frame_range_text_list.append(StringVar())

        for shot in self.project.getShotList():
            cur_shot = Shot(self.project.getDirectory(), shot[1])

            self.shot_text_list[i].set(shot[1])
            self.shot_frame_range_text_list[i].set(cur_shot.getFrameRange())
            if shot[1] not in self.vars_shot_animation:
                self.vars_shot_animation[shot[1]] = StringVar()
            if shot[1] not in self.vars_shot_lighting:
                self.vars_shot_lighting[shot[1]] = StringVar()
            if shot[1] not in self.vars_shot_rendering:
                self.vars_shot_rendering[shot[1]] = StringVar()
            if shot[1] not in self.vars_shot_compositing:
                self.vars_shot_compositing[shot[1]] = StringVar()

            if cur_shot.isDone():
                done_shots += 1

            i += 1

        if done_shots == 1:
            self.done_shots_text.set(str(done_shots) + " done shot (" + str(round(done_shots / len(self.project.getShotList()) * 100)) + "%)")
        else:
            self.done_shots_text.set(str(done_shots) + " done shots (" + str(round(done_shots / len(self.project.getShotList()) * 100)) + "%)")

        self.stats_dict = {}
        for shot in self.project.getShotList():
            shot_stats = []
            shot_stats.append(self.vars_shot_animation[shot[1]].get())
            shot_stats.append(self.vars_shot_lighting[shot[1]].get())
            shot_stats.append(self.vars_shot_rendering[shot[1]].get())
            shot_stats.append(self.vars_shot_compositing[shot[1]].get())
            self.stats_dict[shot[1]] = shot_stats

        with open(self.project_stats_path, "w") as f:
            f.write(json.dumps(self.stats_dict))
