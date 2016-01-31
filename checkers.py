#!/usr/bin/python
from Tkinter import *
import tkMessageBox


class CheckerBoard(Frame):

    BOARD_COL_COUNT = 8
    BOARD_ROW_COUNT = BOARD_COL_COUNT
    X_MARGIN = 40
    Y_MARGIN = 30
    X_WIDTH = 50
    Y_WIDTH = 50
    PIECE_INSET = 10
    PIECE_WIDTH = X_WIDTH - (2 * PIECE_INSET)
    PIECE_HEIGHT = Y_WIDTH - (2 * PIECE_INSET)

    def __init__(self, parent, icoord, prev_itm, moves, illegal, gnum, rnum, is_moved, ocrowns, gcrowns):
        Frame.__init__(self, parent)

        self.parent = parent
        self.icoord = icoord
        self.prev_itm = prev_itm
        self.moves = moves
        self.illegal = illegal
        self.gnum = gnum
        self.rnum = rnum
        self.is_moved = is_moved
        self.ocrowns = ocrowns
        self.gcrowns = gcrowns

        self.InitUI()

    def InitUI(self):

        self.parent.title("Let's play Checkers!")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self,bg="CadetBlue1")

        drag_data = {"x": 0, "y": 0, "item": None}
        init_data = {"x": 0, "y": 0, "item": None}
        final_coord = [0,0]

        red_sqaures = []
        black_squares = []

        for ix in range(1 , self.BOARD_COL_COUNT + 1):
            # ix=1, 2, 3 ... 7, 8

            for iy in range(1 , self.BOARD_ROW_COUNT + 1):
                # iy=1, 2, 3 ... 7, 8
                fill_str = ("tomato", "black")[(iy + ix) % 2]
                tags_str = ("red", "black")[(iy + ix) % 2]
                new_square = canvas.create_rectangle(
                                self.X_MARGIN + ((ix - 1) * self.X_WIDTH),
                                self.Y_MARGIN + ((iy - 1) * self.Y_WIDTH),
                                self.X_MARGIN + (ix * self.X_WIDTH),
                                self.Y_MARGIN + (iy * self.Y_WIDTH),
                                outline=fill_str, fill=fill_str, tags=tags_str
                )
                if tags_str == "red":
                    red_sqaures.append(new_square)  # save a reference to new_square
                else:
                    black_squares.append(new_square)  # save a reference to new_square
                del new_square  # delete the old reference to new_square

        def OnTokenButtonPress(event):
            # record the item and its location
            drag_data["item"] = canvas.find_closest(event.x, event.y)[0]
            drag_data["x"] = event.x
            drag_data["y"] = event.y


            init_data["item"] = drag_data["item"]
            init_data["x"] = drag_data["x"]
            init_data["y"] = drag_data["y"]

            item_below = canvas.find_overlapping(event.x,event.y,event.x,event.y)[0]
            self.icoord = ColumnRowCoords(item_below)


        def OnTokenButtonRelease(event):
            # reset the drag information
            drag_data["item"] = None
            drag_data["x"] = 0
            drag_data["y"] = 0

        def OnTokenMotion(event):
            # compute how much this object has moved
            delta_x = event.x - drag_data["x"]
            delta_y = event.y - drag_data["y"]

            # move the object the appropriate amount
            canvas.move(drag_data["item"], delta_x, delta_y)
            # record the new position
            drag_data["x"] = event.x
            drag_data["y"] = event.y


        def ColumnRowCoords(objID):
            c1, c2 = divmod(objID, self.BOARD_COL_COUNT)
            return [c1 + 1, c2]

        def RectDims(coords):
            x1 = 0
            x2 = 0
            y1 = 0
            y2 = 0

            try:
                assert 1 <= coords[0] <= self.BOARD_COL_COUNT
                assert 1 <= coords[1] <= self.BOARD_ROW_COUNT
                x1 = self.X_MARGIN + ((coords[0] - 1) * self.X_WIDTH)
                x2 = self.X_MARGIN + (coords[0] * self.X_WIDTH)
                y1 = self.Y_MARGIN + ((coords[1] - 1) * self.Y_WIDTH)
                y2 = self.Y_MARGIN + (coords[1] * self.Y_WIDTH)

            except AssertionError as ae:
                pass

            finally:
                return [x1, y1, x2, y2]

        """
        def CenterPieces(dims,x,y):
            cent_x = dims[0] + 25
            cent_y = dims[1] + 25
            del_x = abs(x - cent_x)
            del_y = abs(y - cent_y)

            if x >= dims[0] and x < dims[2] and y >= dims[1] and y < dims[3]:
                if x < cent_x and y < cent_y:
                    canvas.move(init_data["item"],del_x,del_y)
                elif x < cent_x and y > cent_y:
                    canvas.move(init_data["item"],del_x,-1*del_y)
                elif x > cent_x and y < cent_y:
                    canvas.move(init_data["item"],-1*del_x,del_y)
                else:
                    canvas.move(init_data["item"],-1*del_x,-1*del_y)
        """

        #------------------------
        #Initializing Gray pieces
        #------------------------

        gray_pieces = []

        for ix in range(1, 4):
            # ix= 1, 2, 3
            for iy in range(1, self.BOARD_ROW_COUNT + 1):
                # iy=1, 2, 3 ... 7, 8

                if ((iy + ix) % 2) == 1:
                    # (1, 2), (2, 1), (3, 2) ONLY BLACK TILES

                    piece_coords = [self.X_MARGIN + ((ix - 1) * self.X_WIDTH) + self.PIECE_INSET,
                                    self.Y_MARGIN + ((iy - 1) * self.Y_WIDTH) + self.PIECE_INSET,
                                    self.X_MARGIN + (ix * self.X_WIDTH) - self.PIECE_INSET,
                                    self.Y_MARGIN + (iy * self.Y_WIDTH) - self.PIECE_INSET
                                    ]

                    new_piece = canvas.create_oval(*piece_coords,
                                                   outline="SlateGray4", fill="SlateGray4", tags="oval"
                                                   )
                    gray_pieces.append(new_piece)  # save a reference to new_piece
                    del new_piece  # delete the old reference to new_piece

        #------------------------
        #Initializing Red pieces
        #------------------------

        red_pieces = []

        for ix in range((self.BOARD_ROW_COUNT + 1) - 3, self.BOARD_ROW_COUNT + 1):
            # ix= 6, 7, 8
            for iy in range(1, self.BOARD_ROW_COUNT + 1):
                # iy=1, 2, 3 ... 7, 8
                if ((iy + ix) % 2) == 1:
                    # ONLY BLACK TILES

                    piece_coords = [self.X_MARGIN + ((ix - 1) * self.X_WIDTH) + self.PIECE_INSET,
                                    self.Y_MARGIN + ((iy - 1) * self.Y_WIDTH) + self.PIECE_INSET,
                                    self.X_MARGIN + (ix * self.X_WIDTH) - self.PIECE_INSET,
                                    self.Y_MARGIN + (iy * self.Y_WIDTH) - self.PIECE_INSET
                                    ]

                    new_piece = canvas.create_oval(*piece_coords,
                                                   outline="OrangeRed2", fill="OrangeRed2", tags="oval"
                                                   )
                    red_pieces.append(new_piece)  # save a reference to new_piece
                    del new_piece  # delete the old reference to new_piece

        def PieceLogic(event):
            if self.is_moved == True:
                self.is_moved = False

            OnTokenButtonRelease(event)
            bl_tags = canvas.find_withtag("black")
            cur_itm = canvas.find_closest(event.x,event.y)[0]
            item_below = canvas.find_overlapping(event.x,event.y,event.x,event.y)[0]
            itm_tuple = canvas.find_overlapping(event.x,event.y,event.x,event.y)

            final_coord = ColumnRowCoords(item_below)

            row_diff = abs(final_coord[1] - self.icoord[1])
            col_diff = abs(final_coord[0] - self.icoord[0])

            same_colour = False

            if (64 < self.prev_itm < 77) and (64 < cur_itm < 77) and not self.illegal:
                same_colour = True
                tkMessageBox.showinfo(title=None, message="Orange's Turn!")
                if not self.is_moved:
                    delta_x = init_data["x"] - event.x
                    delta_y = init_data["y"] - event.y
                    canvas.move(init_data["item"],delta_x,delta_y)
                    self.is_moved = True

            elif (76 < self.prev_itm < 90) and (76 < cur_itm < 90) and not self.illegal:
                same_colour = True
                tkMessageBox.showinfo(title=None, message="Gray's Turn!")
                if not self.is_moved:
                    delta_x = init_data["x"] - event.x
                    delta_y = init_data["y"] - event.y
                    canvas.move(init_data["item"],delta_x,delta_y)
                    self.is_moved = True

            for item in bl_tags:
                if item == item_below and len(itm_tuple) == 2 and row_diff > 0 and col_diff > 0:
                    sq_dims = RectDims(final_coord)
                    self.moves += 1
                    print "Moves: ", self.moves
                    if final_coord[0] == 1 and cur_itm > 76 and same_colour != True:
                        canvas.itemconfig(cur_itm,fill="OrangeRed4",outline="OrangeRed4")
                        self.ocrowns.append(cur_itm)
                        print "self.ocrowns: ", self.ocrowns
                    elif final_coord[0] == 8 and cur_itm < 77 and same_colour != True:
                        canvas.itemconfig(cur_itm,fill="gray25",outline="gray25")
                        self.gcrowns.append(cur_itm)
                        print "self.gcrowns: ", self.gcrowns

                    gcrn_itm = 0
                    for i in self.gcrowns:
                        if i == cur_itm and same_colour != True:
                            gcrn_itm = i
                            break

                    print
                    print "gcrn_itm: ", gcrn_itm

                    ocrn_itm = 0
                    for i in self.ocrowns:
                        if i == cur_itm and same_colour != True:
                            ocrn_itm = i
                            break

                    print
                    print "ocrn_itm: ", ocrn_itm

                    if col_diff == 2 and row_diff == 2 and self.moves > 1:
                        dpiece_coord = []
                        dpiececol = 0
                        dpiecerow = 0
                        self.prev_itm = cur_itm
                        if final_coord[0] > self.icoord[0] and final_coord[1] > self.icoord[1]:
                            if cur_itm < 77 or ocrn_itm == cur_itm:
                                dpiececol = self.icoord[0] + 1
                                dpiecerow = self.icoord[1] + 1
                                dpiece_coord.append(dpiececol)
                                dpiece_coord.append(dpiecerow)
                            else:
                                self.illegal = True
                                delta_x = init_data["x"] - event.x
                                delta_y = init_data["y"] - event.y
                                canvas.move(init_data["item"],delta_x,delta_y)
                                break
                        elif final_coord[0] > self.icoord[0] and final_coord[1] < self.icoord[1]:
                            if cur_itm < 77 or ocrn_itm == cur_itm:
                                dpiececol = self.icoord[0] + 1
                                dpiecerow = self.icoord[1] - 1
                                dpiece_coord.append(dpiececol)
                                dpiece_coord.append(dpiecerow)
                            else:
                                self.illegal = True
                                delta_x = init_data["x"] - event.x
                                delta_y = init_data["y"] - event.y
                                canvas.move(init_data["item"],delta_x,delta_y)
                                break
                        elif final_coord[0] < self.icoord[0] and final_coord[1] > self.icoord[1]:
                            if cur_itm > 76 or gcrn_itm == cur_itm:
                                dpiececol = self.icoord[0] - 1
                                dpiecerow = self.icoord[1] + 1
                                dpiece_coord.append(dpiececol)
                                dpiece_coord.append(dpiecerow)
                            else:
                                self.illegal = True
                                delta_x = init_data["x"] - event.x
                                delta_y = init_data["y"] - event.y
                                canvas.move(init_data["item"],delta_x,delta_y)
                                break
                        elif final_coord[0] < self.icoord[0] and final_coord[1] < self.icoord[1]:
                            if cur_itm > 76 or gcrn_itm == cur_itm:
                                dpiececol = self.icoord[0] - 1
                                dpiecerow = self.icoord[1] - 1
                                dpiece_coord.append(dpiececol)
                                dpiece_coord.append(dpiecerow)
                            else:
                                self.illegal = True
                                delta_x = init_data["x"] - event.x
                                delta_y = init_data["y"] - event.y
                                canvas.move(init_data["item"],delta_x,delta_y)
                                break

                        if len(dpiece_coord) != 0 and same_colour != True:
                            dims = RectDims(dpiece_coord)
                            dpiece = canvas.find_enclosed(dims[0],dims[1],dims[2],dims[3])
                            if len(dpiece) == 0:
                                delta_x = init_data["x"] - event.x
                                delta_y = init_data["y"] - event.y
                                canvas.move(init_data["item"],delta_x,delta_y)
                                break
                            else:
                                print "Dead piece:", dpiece
                                if (cur_itm < 77 and dpiece[0] > 76) or (cur_itm > 76 and dpiece[0] < 77):
                                    canvas.delete(dpiece)
                                    if dpiece[0] < 77:
                                        self.gnum -= 1
                                        print "gnum: ", self.gnum
                                    else:
                                        self.rnum -= 1
                                        print "rnum: ", self.rnum

                                    if self.gnum == 0 or self.rnum == 0:
                                        if self.gnum > self.rnum:
                                            tkMessageBox.showinfo(title=None,message="Game Over! Gray Wins!")
                                        else:
                                            tkMessageBox.showinfo(title=None,message="Game Over! Orange Wins!")
                                else:
                                    delta_x = init_data["x"] - event.x
                                    delta_y = init_data["y"] - event.y
                                    canvas.move(init_data["item"],delta_x,delta_y)
                                    self.prev_itm = 0
                        break

                    elif col_diff == 1 and row_diff == 1:
                        if (cur_itm > 64 and cur_itm < 77) and cur_itm != gcrn_itm:
                            if final_coord[0] < self.icoord[0]:
                                continue
                        elif (cur_itm > 76 and cur_itm < 90) and cur_itm != ocrn_itm:
                            if final_coord[0] > self.icoord[0]:
                                continue

                        self.prev_itm = cur_itm
                        break

            else:
                if same_colour == False:
                    delta_x = init_data["x"] - event.x
                    delta_y = init_data["y"] - event.y
                    canvas.move(init_data["item"],delta_x,delta_y)



        canvas.tag_bind("oval", "<ButtonPress-1>", OnTokenButtonPress)
        canvas.tag_bind("oval", "<B1-Motion>", OnTokenMotion)
        canvas.tag_bind("oval", "<ButtonRelease-1>", PieceLogic)
        canvas.pack(fill=BOTH, expand=1)


def main():
    root = Tk()
    rturn = False
    gturn = False
    gcount = 0
    rcount = 0
    ex = CheckerBoard(root, [], 0, 0, False, 12, 12, False, [], [])
    root.geometry("480x460+500+200")
    root.mainloop()

if __name__ == '__main__':
    main()